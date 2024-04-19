import asyncio
import pickle
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://my.f2hash.com/login'
user_email = "lasawo9725@rartg.com"
user_password = "Qwerty62982."

# CHROME CONSTANTS

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    ext = paths[1].strip()
    api_key = paths[3].strip()

options.binary_location = chrome_path
# options.add_extension(ext)

#490f5ca2ce767a96c5393566b6ecc29a
#3548e6b7c65b2f3e2f98e7bcf26aaa97


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    try:
        login = await driver.find_element(By.XPATH, '//*[@id="username"]', timeout=30)
        await login.write(user_email)

        password = await driver.find_element(By.XPATH, '//*[@id="passcode"]', timeout=30)
        await password.write(user_password)
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    try:
        click_log_but = await driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[3]/button', timeout=30)
        await asyncio.sleep(1)
        await click_log_but.click()
    except Exception as e:
        print(f'ERROR CLICK BUT LOG \n{e}')

    await asyncio.sleep(2.5)
    await driver.get('https://my.f2hash.com/deposit')

    try:
        choose_crypto = await driver.find_element(By.XPATH, '//*[@id="payment-option-list"]/li[1]/label', timeout=20)
        await asyncio.sleep(1)
        await choose_crypto.click()

        depos_now_but = await driver.find_element(By.XPATH, '//*[@id="deposit-now"]', timeout=20)
        await asyncio.sleep(1.5)
        await depos_now_but.click()
    except Exception as e:
        print(f'ERROR CHOOSE CRYPTO \n{e}')

    try:
        choose_select = await driver.find_element(By.XPATH, '//*[@id="prm-currency-name"]', timeout=20)
        await asyncio.sleep(1.5)
        await choose_select.click()

        choose_USDT = await driver.find_element(By.XPATH, '//*[@id="currency-list"]/li[8]/a', timeout=30)
        await asyncio.sleep(1.5)
        await choose_USDT.click()
    except Exception as e:
        print(f'ERROR CHOOSE USDT \n{e}')

    try:
        input_amount = await driver.find_element(By.XPATH, '//*[@id="prm-amnt"]', timeout=20)
        await asyncio.sleep(1)
        await input_amount.write('50')

        proceed_but = await driver.find_element(By.XPATH, '//*[@id="proceed-btn"]', timeout=30)
        await asyncio.sleep(1.5)
        await proceed_but.click()
    except Exception as e:
        print(f'ERROR PROCEED BUT \n{e}')

    try:
        confirm_but = await driver.find_element(By.XPATH, '//*[@id="confirm-deposit"]', timeout=20)
        await asyncio.sleep(1.5)
        await confirm_but.click()
    except Exception as e:
        print(f'ERROR CONFIRM BUT \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="wallet-address"]', timeout=30)
            address = await address_elem.__getattribute__('value')

            amount_elem = await driver.find_element(By.CLASS_NAME, 'text-soft', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USD", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)