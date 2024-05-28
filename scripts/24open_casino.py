import asyncio
import pyautogui
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://24open-casino.com/user/login'
user_email = "kiracase34@gmail.com"
user_password = "EP2jadJim7hUMfh"

# CHROME CONSTANTS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

options = webdriver.ChromeOptions()
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    api_key_solver = paths[5].strip()
    ext = paths[1].strip()

options.add_extension(ext)
options.binary_location = chrome_path
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})


async def api_connect(driver):
    await asyncio.sleep(1.5)
    windows = await driver.window_handles
    for win in windows:
        await driver.switch_to.window(win)
        await asyncio.sleep(1.5)
        text = await driver.title
        if "2Cap" in text:
            break

    try:
        await js_click(driver, 30, '//*[@id="autoSolveRecaptchaV2"]')
        await js_click(driver, 30, '//*[@id="autoSolveInvisibleRecaptchaV2"]')
        await js_click(driver, 30, '//*[@id="autoSolveRecaptchaV3"]')
        await js_click(driver, 30, '//*[@id="autoSolveHCaptcha"]')

        await input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        await click(driver, 30, '//*[@id="connect"]')
        await asyncio.sleep(4.5)
        alert = await driver.switch_to.alert
        await alert.accept()
    except Exception as e:
        print(f'ERROR CLICK \n{e}')

    windows = await driver.window_handles
    for win in windows:
        await driver.switch_to.window(win)
        await asyncio.sleep(1.5)
        text = await driver.title
        if not("2Cap" in text):
            break


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
    await driver.execute_script("window.open('');")

    await asyncio.sleep(1.5)
    windows = await driver.window_handles
    for win in windows:
        await driver.switch_to.window(win)
        await asyncio.sleep(1.5)
        text = await driver.title
        if not("2Cap" in text):
            break

    await asyncio.sleep(1)
    await driver.get(url, timeout=90)
    await api_connect(driver)

    try:
        await asyncio.sleep(3.5)
        await input_data(driver, 50, '//*[@id="login_login"]', user_email)
        await input_data(driver, 30, '//*[@id="login_password"]', user_password)
        await click(driver, 30, '//*[@id="login_submit"]')
    except Exception as e:
        return {"status":"0", "ext":f"error login {e}"}

    try:
        time_loop = 0
        while True:
            find_check_elem = await driver.find_element(By.XPATH, '(//div[@class="captcha-solver-info"])[4]', timeout=10)
            find_check = await find_check_elem.text
            if ("ена" in find_check) or ("lve" in find_check):
                break
            else:
                if time_loop > 120:
                    return {"status": "0", "ext": "CAPTCHA ERROR"}
                time_loop += 5
                await asyncio.sleep(5)
                print("Wait 5 seconds, captcha solving...")
    except Exception as e:
        print(f'ERROR CHECKBOX')

    await asyncio.sleep(7.5)
    await driver.get('https://24open-casino.com/cabinet/buycredits/choosePayMethod', timeout=90)

    try:
        await click(driver, 30, '(//a[@class="button button--s2 button--t2 transactions__item-button"])[2]')
        await input_data(driver, 30, '//*[@id="deposit_amount"]', '10')
        await click(driver, 30, '//*[@id="deposit_submit"]')
        print('complete')
    except Exception as e:
        return {"status":"0", "ext":f"error min amount input:   {e}"}

    try:
        await asyncio.sleep(5)
        await click(driver, 30, '//*[@id="info"]/form/div[3]/button')
    except Exception as e:
        return {"status":"0", "ext":f"error amount:   {e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '(//a[@target="_blank"])[1]', timeout=60)
            address_href = await address_elem.get_attribute('href')
            print(address_href)
            address = address_href.split('address')[1].replace("/", '')

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="copy"]/nav/div[2]/div/span', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status": "0", "ext": f"error data {e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
