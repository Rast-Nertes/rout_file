import asyncio
import pyautogui
from anticaptchaofficial.imagecaptcha import *
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://21bets.com/account/financials/deposit?modal=login'
user_email = "kiracase34@gmail.com"
user_password = "rRnQ49KN!hDjY7i"


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

    await driver.get(url, timeout=60)

    try:
        await input_data(driver, 30, '//input[@name="email"]', user_email)
        await input_data(driver, 30, '//input[@name="password"]', user_password)
        await click(driver, 30, '//*[@id="app"]/div[1]/div/div[2]/div/div/div[2]/div[1]/div[2]/form/div[2]/button')
    except Exception as e:
        return {"status": "0", "ext": f"Login error \n{e}"}

    try:
        await asyncio.sleep(2.4)
        find_frame = await driver.find_element(By.XPATH, '//iframe[@title="MyAccount"]', timeout=20)
        await asyncio.sleep(0.6)
        iframe_doc = await find_frame.get_attribute('src')
        await driver.get(iframe_doc)
    except Exception as e:
        print(f'ERROR CHECKBOX \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        try:
            amount_elem = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/a[10]/div/div[2]/div[1]/span[2]', timeout=30)
            amount = await amount_elem.text

            try:
                await click(driver, 30, '//img[@alt="USDT (TRC20)"]')
            except Exception as e:
                return {"status": "0", "ext": f"CHOOSE TRC20 \n{e}"}

            await asyncio.sleep(4.5)
            address_elem = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/div[2]/div/div/div[1]/strong', timeout=30)
            address = await address_elem.text

            return {
                "address": address,
                "amount": amount.replace("\xa0", "").replace("$", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
