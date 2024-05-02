import asyncio
import pyautogui
from twocaptcha import TwoCaptcha
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://bspin.io/ru/login'
user_email = "kiracase34@gmail.com"
user_password = "Kiramira123!"

# CHROME CONSTANTS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    ext = paths[1].strip()

options.binary_location = chrome_path
options.add_extension(ext)


async def click(driver, time, XPATH):
    find_click = await driver.find_element(By.XPATH, XPATH, timeout=time)
    await asyncio.sleep(1.5)
    await find_click.click()


async def input_data(driver, time, XPATH, data):
    find_input = await driver.find_element(By.XPATH, XPATH, timeout=time)
    await find_input.clear()
    await find_input.write(data)


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    handles = await driver.window_handles
    print(handles)
    for handle in handles:
        await driver.switch_to.window(handle)
        title = await driver.title
        if "2Cap" in title:
            break

    try:
        await input_data(driver, 30, '//input[@name="apiKey"]', api_key)
        await click(driver, 30, '//*[@id="connect"]')
    except Exception as e:
        print(f'ERROR CONNECT API \n{e}')

    await asyncio.sleep(6.5)
    pyautogui.press('enter')
    await asyncio.sleep(2.5)

    handles = await driver.window_handles
    for handle in handles:
        await driver.switch_to.window(handle)
        title = await driver.title
        if ("коин" in title) or ("bspin" in title):
            if "bspin" in title:
                await driver.refresh()
                break

    await asyncio.sleep(3.5)

    try:
        await input_data(driver, 30, '//*[@id="content"]/div/div[2]/div[2]/div/form/div[1]/input', user_email)
        await input_data(driver, 30, '//*[@id="content"]/div/div[2]/div[2]/div/form/div[2]/input', user_password)
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        await click(driver, 30, '//div[@class="captcha-solver captcha-solver_inner"]')
    except Exception as e:
        print(f'ERROR CLICK SOLVE CAPTCHA \n{e}')

    while True:
        try:
            find_captcha_text = await driver.find_element(By.XPATH, '//div[@class="captcha-solver-info"]', timeout=10)
            text = await find_captcha_text.text
            if "шает" in text:
                await asyncio.sleep(5)
                print("Wait 5 seconds...")
            else:
                print("Solve")
                break
        except:
            print("Solve")
            break

    await asyncio.sleep(4.5)
    try:
        await click(driver, 30, '//button[@class="xbtn large login-btn acc-btn login-page"]')
    except Exception as e:
        print(f'ERROR CLICK LOG BUT \n{e}')

    try:
        await asyncio.sleep(5.5)
        await click(driver, 30, '//*[@id="content"]/div[6]/div[1]/a')
        await click(driver, 30, '//*[@id="user-action-buttons"]/a[2]')
    except Exception as e:
        print(f'ERROR CLICK \n{e}')

    try:
        await click(driver, 30, '//*[@id="desktop-header-container"]/div/div/div/div[2]/div')
        await click(driver, 30, '//*[@id="desktop-header-container"]/div/div/div/div[2]/div[2]/div[2]')
    except Exception as e:
        print(f'ERROR CLICK \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="desktop-header-container"]/div/div/div/div[4]/button/div/span[2]', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="desktop-header-container"]/div/div/div/div[3]/div[1]/span', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace('Мин. депозит', '').replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
