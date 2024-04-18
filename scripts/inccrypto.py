import asyncio
import pickle
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://inccrypto.net/auth-login'
user_email = "lasawo9725@rartg.com"
user_password = "Qwerty62982."

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
        input_email = await driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/section/div/div/div/div/div/form/div/div[1]/div/div/input', timeout=20)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/section/div/div/div/div/div/form/div/div[2]/div/div/input', timeout=20)
        await input_pass.write(user_password)
    except Exception as e:
        print(f'ERROR INPUT LOG DATA \n{e}')

    try:
        click_log = await driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/section/div/div/div/div/div/form/div/div[4]/div', timeout=30)
        await asyncio.sleep(1.5)
        await click_log.click()
    except Exception as e:
        print(f'ERROR CLICK LOG BUT \n{e}')

    await asyncio.sleep(2.5)
    await driver.get('https://inccrypto.net/profile/deposits')

    try:
        input_amount = await driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/section/div/div/div[2]/div/section[1]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/input', timeout=20)
        await input_amount.write('1')

        click_choose = await driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/section/div/div/div[2]/div/section[1]/div[2]/div/div/div[2]/div/div[3]/div[2]/div/div[1]/input', timeout=20)
        await asyncio.sleep(1)
        await click_choose.click()

        choose_trc20 = await driver.find_element(By.XPATH, '/html/body/div[6]/div[1]/div[1]/ul/li[1]/span', timeout=30)
        await asyncio.sleep(1)
        await choose_trc20.click()
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    try:
        convert_but = await driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/section/div/div/div[2]/div/section[1]/div[2]/div/div/div[2]/div/div[5]/div/button', timeout=20)
        await asyncio.sleep(1)
        await convert_but.click()
    except Exception as e:
        print(f'ERROR CONV BUT \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/section/div/div/div[2]/div/section[1]/div[2]/div/div/div[2]/div/div[5]/div[2]/span', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/section/div/div/div[2]/div/section[1]/div[2]/div/div/div[2]/div/div[4]/div/span[2]', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT-TRC20", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
