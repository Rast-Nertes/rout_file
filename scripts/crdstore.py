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
        print(f"ERROR CHOOSE \n{e}")

    try:
        input_first_name = await driver.find_element(By.ID, 'billing_first_name', timeout=30)
        await input_first_name.write("Kira")

        input_last_name = await driver.find_element(By.ID, 'billing_email', timeout=30)
        await input_last_name.write(user_login)

        sleep(1.5)
        terms_click = await driver.find_element(By.ID, 'terms', timeout=30)
        await terms_click.click()
    except Exception as e:
        print(f"ERROR INPUT DATA \n{e}")

    try:
        choose_wallet = await driver.find_element(By.ID, 'mcc_currency_id', timeout=30)
        await asyncio.sleep(3.5)
        await choose_wallet.click()

        for _ in range(6):
            pyautogui.press('down')
            sleep(0.5)
        pyautogui.press('enter')
        sleep(0.5)
    except Exception as e:
        print(f"ERROR CHOOSE \n{e}")

    try:
        sleep(1.5)
        place_order = await driver.find_element(By.ID, 'place_order', timeout=20)
        await place_order.click()
    except Exception as e:
        print(f"ERROR TERMS \n{e}")


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        try:
            amount_element = await driver.find_element(By.XPATH, '//*[@id="post-10"]/div/div/div/div[3]/div/p/span[1]/span/input', timeout=30)
            amount_attribute = await amount_element.__getattribute__('value')
            amount = str(amount_attribute).replace("USDT_TRON", "").replace(" ", '')

            address_element = await driver.find_element(By.XPATH, '//*[@id="post-10"]/div/div/div/div[3]/div/p/span[2]/span/input', timeout=30)
            address = await address_element.__getattribute__('value')
        except Exception as e:
            print(f"DATA ERROR \n{e}")
            return "Not work data"

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
