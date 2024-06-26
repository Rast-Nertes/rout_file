import asyncio
import pyautogui
from selenium_driverless.scripts.switch_to import SwitchTo
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://raceoption.com/en/login'
user_email = "kejokan542@haislot.com"
user_password = "Qwerty17"

# CHROME CONSTANTS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

options = webdriver.ChromeOptions()
# user_agent = UserAgent()
# options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    ext = paths[1].strip()

options.binary_location = chrome_path
options.add_extension(ext)


async def switch_to_captcha_window(driver):
    handles = await driver.window_handles
    print(handles)
    for handle in handles:
        await driver.switch_to.window(handle)
        title = await driver.title
        if "2Cap" in title:
            break


async def switch_to_window(driver, name_window):
    handles = await driver.window_handles
    for handle in handles:
        await driver.switch_to.window(handle)
        await asyncio.sleep(1.5)
        title = await driver.title
        if name_window in title:
            break


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
    await asyncio.sleep(2)
    await driver.execute_script("window.open('about:blank', '_blank');")
    await asyncio.sleep(1.5)

    await switch_to_window(driver, "about")

    await asyncio.sleep(1.5)

    await driver.get(url, timeout=60)

    await asyncio.sleep(1.5)
    await switch_to_captcha_window(driver)

    try:
        await click(driver, 30, '//*[@id="autoSolveRecaptchaV2"]')
        await click(driver, 30, '//*[@id="autoSolveInvisibleRecaptchaV2"]')
        await click(driver, 30, '//*[@id="autoSolveRecaptchaV3"]')
        await click(driver, 30, '//*[@id="config-form"]/div[2]/table/tbody/tr[4]/td[1]/div/div[1]')
        await click(driver, 30, '//*[@id="config-form"]/div[2]/table/tbody/tr[4]/td[1]/div/div[2]/div/div[2]')
        await input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        await click(driver, 30, '//*[@id="connect"]')
        await asyncio.sleep(4.5)
        alert = await driver.switch_to.alert
        await alert.accept()
    except Exception as e:
        print(f'ERROR CLICK \n{e}')

    await switch_to_window(driver, 'ace')

    try:
        await input_data(driver, 30, '//*[@id="email"]', user_email)
        await asyncio.sleep(5.5)
        await input_data(driver, 30, '//*[@id="pass"]', user_password)
        await asyncio.sleep(5.5)
        await click(driver, 30, '/html/body/div[1]/main/section/div/div/div/div[2]/div[2]/form/div[3]/div[2]/button')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        time_loop = 0
        while True:
            find_check = await driver.find_element(By.XPATH, '/html/body/div[1]/main/section/div/div/div/div[2]/div[2]/div[3]/div[2]', timeout=10)
            check_text = await find_check.text
            if ("ена" in check_text) or ("lve" in check_text):
                await click(driver, 30, '/html/body/div[1]/main/section/div/div/div/div[2]/div[2]/form/div[3]/div[2]/button ')
                break
            else:
                if time_loop > 120:
                    return {"status": "0", "ext": "CAPTCHA ERROR"}
                time_loop += 5
                await asyncio.sleep(5)
                print("Wait 5 seconds, captcha solving...")
    except Exception as e:
        print(f'ERROR CHECKBOX \n{e}')

    await asyncio.sleep(3.5)
    await driver.get('https://raceoption.com/trading/deposit')

    try:
        await click(driver, 30, '/html/body/app-root/app-account-funding/div/div/app-deposit-methods/div[2]/div[3]')
    except Exception as e:
        return f'ERROR CHOOSE CRYPTOPAY \n{e}'

    try:
        await asyncio.sleep(1)
        await click(driver, 30, '//*[@id="app-scroll"]/ul/li[3]')
        await asyncio.sleep(1)
        await click(driver, 30, '/html/body/app-root/app-account-funding/div/div/app-deposit-amount/ul/li[1]/button')
    except Exception as e:
        print(f'ERORR CLICKs \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            amount_elem = await driver.find_element(By.XPATH, '//*[@id="app-scroll"]/app-crypto-deposit-info/div/div/div[2]/app-copy-button/div/span', timeout=30)
            amount = await amount_elem.text

            address_elem = await driver.find_element(By.XPATH, '//*[@id="app-scroll"]/app-crypto-deposit-info/div/div/div[3]/div[2]/app-copy-button/div/span', timeout=30)
            address = await address_elem.text

            return {
                "address": address.replace(" ", ''),
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
