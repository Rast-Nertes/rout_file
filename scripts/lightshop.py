import time
import pyautogui
from flask import jsonify
from fake_useragent import UserAgent
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
import asyncio

#CONSTANS

url = 'https://lightshop.su/'
user_login = 'kiracase34@gmail.com'
user_pass = 'oleg34oleg'

#CHROME OPTIONS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")

async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await driver.get(url)
        await driver.refresh()
        await driver.maximize_window()

        try:
           #time.sleep(100)
            choose_product = await driver.find_element(By.CSS_SELECTOR, 'div.table-responsive > table > tbody > tr:nth-child(13) > td.text-center > a > i', timeout=10)
            await driver.execute_script("arguments[0].click();", choose_product)
        except Exception as e:
            print(f'CHOOSE PRODUCT ERROR \n{e}')

        try:
            input_email_in_product = await driver.find_element(By.CSS_SELECTOR, '#order > table > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=text]', timeout=10)
            time.sleep(2)
            await input_email_in_product.write(user_login)
        except Exception as e:
            print(f"INPUT EMAIL ERROR \n{e}")

        pyautogui.moveTo(1000, 500)
        pyautogui.click()

        time.sleep(2)

        pyautogui.moveTo(1000, 600)
        pyautogui.click()

        try:
            start_buy = await driver.find_element(By.CSS_SELECTOR, '#order > footer > button', timeout=40)
            time.sleep(2)
            await driver.execute_script("arguments[0].click();", start_buy)
        except Exception as e:
            print(f"START BUY BUTTON ERROR \n{e}")
            return "Not work"

        try:
            choose_tether = await driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/form[2]/div[13]', timeout=40)
            time.sleep(3)
            await choose_tether.click()
        except Exception as e:
            print(f"CHOOSE TETHER ERROR \n{e}")
            return "Not work"

        try:
            accept = await driver.find_element(By.CSS_SELECTOR, 'div.payment-container > div.popup__bg.active > div > div > input', timeout=20)
            time.sleep(5)
            await driver.execute_script("arguments[0].click();", accept)
        except Exception as e:
            print(f"CONTINUE BUTTON ERROR \n{e}")
            return "Not work"

        try:
            amount_element = await driver.find_element(By.ID, 'pay_amount', timeout=10)
            amount = await amount_element.text

            address_element = await driver.find_element(By.ID, 'crypto_address', timeout=10)
            address = await address_element.text
        except Exception as e:
            print(f"DATA ERROR \n{e}")
            return "Not work"

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }

def wallet():
    wallet_data = asyncio.run(get_wallet())
    #print(wallet_data)
    return jsonify(wallet_data)
