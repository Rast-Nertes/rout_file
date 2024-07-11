import asyncio
import re
import pyautogui
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://bestedplg.com/karton-cc-cvv-usa/'
user_email = "kiracase34@gmail.com"
user_password = "r7R6Lc2Y7hvz95s"

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
    ext = paths[4].strip()

options.add_extension(ext)
options.binary_location = chrome_path
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})


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
        add_to_cart = await driver.find_element(By.CSS_SELECTOR, 'div.summary.entry-summary > form > button', timeout=20)
        await asyncio.sleep(1.5)
        await driver.execute_script("arguments[0].click();", add_to_cart)
    except Exception as e:
        return {"status": "0", "ext": f"Login error \n{e}"}

    await asyncio.sleep(3)
    await driver.get('https://bestedplg.com/checkout/', timeout=60)
    await asyncio.sleep(3)

    try:
        choose_trc20 = await driver.find_element(By.ID, 'headingTwo', timeout=20)
        await asyncio.sleep(1.5)
        await driver.execute_script("arguments[0].click();", choose_trc20)
    except Exception as e:
        return {"status": "0", "ext": f"DEPOS BUT \n{e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.ID, 'usdtadr', timeout=20)
            address = await address_elem.get_attribute('value')

            amount_elem = await driver.find_element(By.ID, 'usdtquan', timeout=20)
            amount = await amount_elem.get_attribute('value')

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
