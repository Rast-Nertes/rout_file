import asyncio
import pyautogui
from anticaptchaofficial.imagecaptcha import *
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://cryptorino.io/en/?type=login&modal=user'
user_email = "kiracase34@gmail.com"
user_password = "dLgPAy9D5NMn4DT"


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

# options.add_extension(ext)
options.binary_location = chrome_path


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
    await driver.get(url, timeout=60)

    try:
        await input_data(driver, 30, '//input[@name="email"]', user_email)
        await input_data(driver, 30, '//input[@name="password"]', user_password)
        await click(driver, 30, '/html/body/div[4]/div/div/div/div/div[2]/form/button')
    except Exception as e:
        return {"status": "0", "ext":f"login error \n{e}"}

    try:
        await click(driver, 30, '//*[@id="currency-selector-button"]')
        await click(driver, 30, '//i[@class="currency-icon currency-icon-usdt"]')
        await click(driver, 30, '//*[@id="mainNav"]/div/div[3]/div/div/a')
    except Exception as e:
        return {"status":"0", "ext":f"error depos but \n{e}"}

    try:
        await click(driver, 30, '//img[@class="img method-usdt-trx"]')
    except Exception as e:
        return {"status": "0", "ext": f"error choose trc20 \n{e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="cryptoAddress"]', timeout=30)
            address = await address_elem.text

            return {
                "address": address,
                "amount": "0.01",
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data \n{e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
