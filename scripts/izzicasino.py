import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://izzicasino.com/ru/signin'
user_email = "kiracase34@gmail.com"
user_password = "iXm2754qDUKg-#n"

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
# options.add_extension(ext)


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

    try:
        await input_data(driver, 30, '//input[@name="email"]', user_email)
        await input_data(driver, 30, '//input[@name="password"]', user_password)
    except Exception as e:
        print(f'ERROR CAPTCHA SOLVE \n{e}')

    while True:
        try:
            await click(driver, 10, '//button[@type="submit"]')
            await asyncio.sleep(1)
        except:
            break

    try:
        await click(driver, 30, '//*[@id="popup-deposit"]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[1]/div[2]/div/div[4]')
    except Exception as e:
        print(f'ERROR CHOOSE CRYPTO \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            amount_elem = await driver.find_element(By.CLASS_NAME, 'payment-area__info-btc__date_exchange-rate', timeout=30)
            amount = await amount_elem.text

            address_elem = await driver.find_element(By.CLASS_NAME, 'input-field__button input-field__button--copy', timeout=30)
            await asyncio.sleep(1.5)
            await address_elem.click()

            await asyncio.sleep(3.5)
            address = pyperclip.paste()

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace("\xa0", '').replace(" ", ""),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
