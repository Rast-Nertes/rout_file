from time import sleep
import pyautogui
from flask import jsonify
from fake_useragent import UserAgent
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
import asyncio

#CONSTANS

url = 'https://crdstore.cc/buy/worldwide-cvv/'
user_login = 'kiracase34@gmail.com'
user_pass = 'kirakira123'

#CHROME OPTIONS

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.binary_location = chrome_path


async def login(driver):
    await driver.get(url)
    await driver.maximize_window()

    try:
        choose_country = await driver.find_element(By.ID, 'wd-add-to-cart', timeout=50)
        await choose_country.click()
    except Exception as e:
        return {"status":"0", "ext":f"error choose {e}"}

    try:
        await asyncio.sleep(5)
        input_first_name = await driver.find_element(By.ID, 'billing_first_name', timeout=30)
        await input_first_name.write("Kira")

        input_last_name = await driver.find_element(By.ID, 'billing_email', timeout=30)
        await input_last_name.write(user_login)

        await asyncio.sleep(3)
        terms_click = await driver.find_element(By.ID, 'terms', timeout=30)
        await terms_click.click()
    except Exception as e:
        return {"status":"0", "ext":f"error input data {e}"}

    try:
        choose_wallet = await driver.find_element(By.ID, 'mcc_currency_id', timeout=30)
        await asyncio.sleep(3)
        await driver.execute_script("arguments[0].value = 'USDT_TRON';", choose_wallet)
        await asyncio.sleep(1.5)
    except Exception as e:
        return {"status":"0", "ext":f"error choose trc20{e}"}

    try:
        sleep(1.5)
        place_order = await driver.find_element(By.ID, 'place_order', timeout=20)
        await place_order.click()
    except Exception as e:
        return {"status":"0", "ext":f"error terms {e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        try:
            amount_element = await driver.find_element(By.XPATH, '//*[@id="post-10"]/div/div/div/div[3]/div/p/span[1]/span/input', timeout=30)
            amount_attribute = await amount_element.get_attribute('value')
            amount = str(amount_attribute).replace("USDT_TRON", "").replace(" ", '')

            address_element = await driver.find_element(By.XPATH, '//*[@id="post-10"]/div/div/div/div[3]/div/p/span[2]/span/input', timeout=30)
            address = await address_element.get_attribute('value')
        except Exception as e:
            return {"status": "0", "ext": f"error data {e}"}

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
