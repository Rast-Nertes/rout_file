import asyncio
import pyperclip
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://game777win.com/ru/login'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

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
        input_email = await driver.find_element(By.XPATH, '//*[@id="email"]', timeout=30)
        await input_email.write(user_email)

        input_password = await driver.find_element(By.XPATH, '//*[@id="password"]', timeout=20)
        await input_password.write(user_password)

        click_log = await driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div[2]/div/div/div[2]/div[1]/div/div/form/button', timeout=20)
        await asyncio.sleep(1)
        await click_log.click()
    except Exception as e:
        print(f'ERROR LOGIN SESSION \n{e}')

    await asyncio.sleep(3.5)
    await driver.get('https://game777win.com/ru/profile/cash')

    try:
        choose_trc20 = await driver.find_element(By.XPATH, '//img[@alt="USDT TRC-20"]', timeout=20)
        await asyncio.sleep(1)
        await choose_trc20.click()
    except:
        return 'Login error. Check script.'

    try:
        click_copy_but = await driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div/div/button', timeout=20)
        await asyncio.sleep(1)
        await click_copy_but.click()
    except Exception as e:
        print(f'ERROR CLICK COPY ADDRESS \n{e}')

    return None


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return "Login error. Check script."

        await asyncio.sleep(2.5)
        try:
            address = pyperclip.paste()

            amount_elem = await driver.find_element(By.XPATH, '/html/body/div[1]/div/div[4]/div/div[2]/div[2]/div[2]/div[1]/div[1]/div[3]/span[1]', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("€", '').replace("\xa0", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)

