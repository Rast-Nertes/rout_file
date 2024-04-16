import asyncio
import pickle
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://vavadapot.com/ru/login'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

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

options.binary_location = chrome_path


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    await asyncio.sleep(2.5)
    await driver.refresh()
    await asyncio.sleep(2)

    try:
        input_email = await driver.find_element(By.XPATH, '//*[@id="_username"]', timeout=50)
        await asyncio.sleep(0.5)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.XPATH, '//*[@id="_password"]', timeout=20)
        await asyncio.sleep(0.5)
        await input_pass.write(user_password)
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    try:
        click_log = await driver.find_element(By.XPATH, '//*[@id="_submit"]', timeout=20)
        await asyncio.sleep(0.5)
        await click_log.click()
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    await asyncio.sleep(2.5)
    await driver.get('https://vavadapot.com/en/profile/deposit/form/tether_trc20')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div/fieldset[1]/div[2]/input', timeout=30)
            address = await address_elem.__getattribute__('value')

            amount_elem = await driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div/fieldset[1]/p[3]', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("Minimum deposit is", '').replace("$", '').replace(" ", '') + "00",
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)