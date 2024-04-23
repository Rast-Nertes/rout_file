import asyncio
import pickle
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://chipstars.bet/en/login'
user_email = "kiracase34@gmail.com"
user_password = "t8!qnYDF@aE36*"

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

options.binary_location = chrome_path


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    try:
        await asyncio.sleep(2.4)
        find_frame = await driver.find_elements(By.TAG_NAME, 'iframe')
        await asyncio.sleep(0.6)
        iframe_doc = await find_frame[0].content_document
        click_checkbox = await iframe_doc.find_element(By.XPATH, '//*[@id="challenge-stage"]/div/label/input', timeout=20)
        await click_checkbox.click()
    except Exception as e:
        print(f'ERROR CHECKBOX \n{e}')

    try:
        input_email = await driver.find_element(By.XPATH, '//*[@id="login-field"]', timeout=30)
        await input_email.write(user_email)

        input_password = await driver.find_element(By.XPATH, '//*[@id="form-password"]', timeout=20)
        await input_password.write(user_password)
    except Exception as e:
        print(f'ERROR LOG DATA \n{e}')

    try:
        click_log_but = await driver.find_element(By.XPATH, '//*[@id=":r0:"]', timeout=30)
        await asyncio.sleep(1.5)
        await click_log_but.click()
    except Exception as e:
        print(f"ERROR CLICK LOG BUT \n{e}")

    await asyncio.sleep(3.5)
    await driver.get('https://chipstars.bet/en')

    try:
        click_depos_but = await driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div/nav/div[2]/div/div[2]/div/div[2]/div[1]/button/span', timeout=20)
        await asyncio.sleep(1.5)
        await click_depos_but.click()
    except Exception as e:
        input_elem = await driver.find_element(By.XPATH, '//*[@id="login-field"]', timeout=30)
        if input_elem:
            return {"status": "0", "ext":"Login error. Check script."}

    try:
        input_amount = await driver.find_element(By.NAME, 'depositAmount', timeout=20)
        await input_amount.clear()
        await input_amount.write('10')

        click_depos_now_but = await driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div/div[2]/div/div/div[1]/div/button/span', timeout=20)
        await asyncio.sleep(1.5)
        await click_depos_now_but.click()
    except Exception as e:
        print(f'ERROR DEPOS BUT \n{e}')

    try:
        choose_crypto = await driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div/div[2]/div/div/div[2]/div/div/p[2]', timeout=20)
        await asyncio.sleep(1.5)
        await choose_crypto.click()

        choose_trc20 = await driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div/div[2]/div/div/div[2]/div/ul/li[8]/div', timeout=20)
        await asyncio.sleep(1.5)
        await choose_trc20.click()
    except Exception as e:
        print(f'ERROR CHOOSE  CRYPTO \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.ID, 'outlined-adornment-password', timeout=30)
            address = await address_elem.__getattribute__("value")

            amount_elem = await driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div/div[2]/div/div/div[3]/div/div[3]/h4[1]', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("$", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)