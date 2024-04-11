import asyncio
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

url = 'https://www.cloudbet32.com/ru/auth/sign-in'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    ext = paths[1].strip()

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.binary_location = chrome_path
# options.add_extension(ext)


async def login(driver):
    # await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await driver.get(url, timeout=60)
    await driver.maximize_window()

    try:
        input_email = await driver.find_element(By.XPATH, '//*[@id="login"]', timeout=20)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.XPATH, '//*[@id="password"]', timeout=20)
        await input_pass.write(user_password)

        click_log_but = await driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/form/div[3]/div/button', timeout=20)
        await asyncio.sleep(1)
        await click_log_but.click()
    except Exception as e:
        print(f'ERROR LOG \n{e}')

    try:
        input_amount = await driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/header/div/div/div[4]/button[3]', timeout=20)
        await asyncio.sleep(1)
        await input_amount.click()

        choose_coint = await driver.find_element(By.XPATH, '//*[@id="Coin"]', timeout=20)
        await asyncio.sleep(1)
        await choose_coint.click()

        choose_tet = await driver.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul/li[25]', timeout=20)
        await asyncio.sleep(1)
        await choose_tet.click()
    except Exception as e:
        print(f"ERROR CHOOSE TETHER \n{e}")

    try:
        choose_net = await driver.find_element(By.XPATH, '//*[@id="Network"]', timeout=20)
        await asyncio.sleep(1)
        await choose_net.click()

        choose_tron = await driver.find_element(By.XPATH, '//*[@id="menu-"]/div[3]/ul/li[6]', timeout=20)
        await asyncio.sleep(1)
        await choose_tron.click()
    except Exception as e:
        print(f'ERROR CHOOSE NET \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(5.5)
        try:
            try:
                address_elem = await driver.find_element(By.XPATH, '/html/body/div[7]/div[3]/div/div[1]/div/div[3]/div/div[2]/button/div[1]/p[2]', timeout=30)
                address = await address_elem.text
            except:
                address_elem = await driver.find_element(By.XPATH, '/html/body/div[6]/div[3]/div/div[1]/div/div[3]/div/div[2]/button/div[1]/p[2]', timeout=30)
                address = await address_elem.text
            return {
                "address": address,
                "amount": '0.01',
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
