import asyncio
import pyautogui
from hcaptcha_solver import hcaptcha_solver
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://starbets.io/'
user_email = "rwork875@gmail.com"
user_password = "00001111Rw"

# CHROME CONSTANTS

# proxy_address = "45.130.254.133"
# proxy_login = 'K0nENe'
# proxy_password = 'uw7RQ3'
# proxy_port = 8000

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    api_key_solver = paths[5].strip()
    ext = paths[4].strip()

options.add_extension(ext)
options.binary_location = chrome_path
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})


async def api_connect():
    await asyncio.sleep(0.4)
    pyautogui.moveTo(1730, 75)
    pyautogui.click()

    await asyncio.sleep(1)

    for _ in range(2):
        pyautogui.press('down')
        await asyncio.sleep(0.15)
    pyautogui.press('enter')

    await asyncio.sleep(1.5)

    for _ in range(4):
        pyautogui.press('tab')
        await asyncio.sleep(0.15)

    await asyncio.sleep(2.5)
    pyautogui.typewrite(api_key_solver, 0.05)
    await asyncio.sleep(1)

    pyautogui.moveTo(1730, 15)
    pyautogui.click()
    await asyncio.sleep(2)


async def solve_captcha(driver):
    try:
        time_ = 0
        await asyncio.sleep(5.4)
        find_frame = await driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/iframe', timeout=10)
        await asyncio.sleep(0.6)
        iframe_doc = await find_frame.content_document
        click_checkbox = await iframe_doc.find_element(By.XPATH, '//button[@class="rc-button goog-inline-block rc-button-reload"]', timeout=20)
        await click_checkbox.click()

        while True:
            if time_ >= 35:
                await click_checkbox.click()

            find_check = await iframe_doc.find_element(By.XPATH, '//button[@class="rc-button goog-inline-block rc-button-reload"]', timeout=10)
            if find_check:
                await asyncio.sleep(5)
                time_ += 5
                print("Wait 5 seconds, captcha solving...")
            else:
                break
    except Exception as e:
        print(f'ERROR CHECKBOX \n{e}')


async def js_click(driver, time, XPATH):
    find_click = await driver.find_element(By.XPATH, XPATH, timeout=time)
    await asyncio.sleep(1.5)
    await driver.execute_script("arguments[0].click();", find_click)


async def click(driver, time, XPATH):
    find_click = await driver.find_element(By.XPATH, XPATH, timeout=time)
    await asyncio.sleep(1.5)
    await find_click.click()


async def input_data(driver, time, XPATH, data):
    find_input = await driver.find_element(By.XPATH, XPATH, timeout=time)
    await find_input.clear()
    await asyncio.sleep(0.5)
    await find_input.write(data)


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await api_connect()
    await driver.get(url, timeout=60)

    try:
        await click(driver, 30, '//*[@id="root"]/div/div/div[1]/div[3]/div[1]/button')
        await input_data(driver, 30, '//*[@id="email"]', user_email)
        await input_data(driver, 30, '//*[@id="password"]', user_password)
        await click(driver, 30, '//*[@id="root"]/div/div[2]/div[2]/form/div[2]/button')
    except Exception as e:
        print(f'ERROR LOG CLICK \n{e}')

    await solve_captcha(driver)

    try:
        find_error = await driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/form/div[2]/div[4]', timeout=10)
        error = await find_error.text
        if "wrong" in error:
            await click(driver, 30, '//*[@id="root"]/div/div[2]/div[2]/form/div[2]/button')
            await solve_captcha(driver)
    except:
        pass

    await asyncio.sleep(3.5)

    try:
        await click(driver, 30, '//*[@id="root"]/div/div/div[1]/div[3]/div[1]/div[2]')
        await click(driver, 30, '//*[@id="root"]/div/div[2]/div[2]/div[3]/div[2]/div[2]/div[1]/div/div[1]/div')
        await click(driver, 30, '//*[@id="root"]/div/div[2]/div[2]/div[3]/div[2]/div[2]/div[1]/div/div[2]/div/div[5]')
        await click(driver, 30, '//*[@id="root"]/div/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div/div[1]')
        await click(driver, 30, '//*[@id="root"]/div/div[2]/div[2]/div[3]/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/p')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[3]/div[2]/div[3]/div[1]/div/p', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[3]/div[2]/div[3]/div[2]/p', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
