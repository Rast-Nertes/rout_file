import asyncio
import pyautogui
from anticaptchaofficial.imagecaptcha import *
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://sol.casino/signin'
user_email = "kiracase34@gmail.com"
user_password = "hQj8@7DJrn2HWY."

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
    api_key_solver = paths[5].strip()
    api_anti = paths[2].strip()
    ext = paths[4].strip()

options.binary_location = chrome_path
options.add_extension(ext)


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
    await driver.get(url, timeout=90)

    try:
        await input_data(driver, 30, '//*[@id="email"]', user_email)
        await input_data(driver, 30, '//*[@id="password"]', user_password)
        await click(driver, 30, '//*[@id="app"]/div[5]/div/div/div[1]/div/div/div/div/div[2]/form/div[1]/div[2]/button')
    except Exception as e:
        return {"status": "0", "ext": f"error login \n{e}"}

    try:
        await click(driver, 30, '//*[@id="app"]/div[6]/div/div/div/div/div[1]/div[2]/div/div[3]/div/div/div[2]/div[6]')
        await click(driver, 30, '//*[@id="app"]/div[6]/div/div/div/div/div[1]/div[2]/div/div[4]/div/div[2]/div[3]')
    except Exception as e:
        return {"status": "0", "ext": f"error choose trc20 \n{e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(8.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//div[@class="payment-crypto__wallet-address"]', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//p[@class="payment-crypto__text-sum"]', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address.replace(" ", ""),
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status": "0", "ext": f"error login \n{e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
