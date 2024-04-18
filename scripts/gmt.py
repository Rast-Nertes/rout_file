import asyncio
import pickle
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://app.gmt.io/buy/crypto?currency=USDT'
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
        input_email = await driver.find_element(By.XPATH, '//*[@id="email"]', timeout=30)
        await input_email.write(user_email)

        input_email = await driver.find_element(By.XPATH, '//*[@id="password"]', timeout=20)
        await input_email.write(user_password)
    except Exception as e:
        print(f'ERROR INPUT \n{e}')

    try:
        login_button = await driver.find_element(By.XPATH, '//*[@id="app"]/login/auth-login/auth-layout/div/div[2]/card/div/div[1]/div[3]/login-form/form/div[3]/button', timeout=20)
        await asyncio.sleep(1)
        await login_button.click()
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        close = await driver.find_element(By.XPATH, '//*[@id="html"]/body/modal-container/div[2]/div/board-miner-create-modal/modal/div/button/icon-box/span', timeout=10)
        await asyncio.sleep(1.5)
        await driver.execute_script("arguments[0].click();", close)

        close_1 = await driver.find_element(By.XPATH, '//*[@id="html"]/body/consent-popup/div/div/div[2]/button[1]', timeout=10)
        await asyncio.sleep(1.5)
        await driver.execute_script("arguments[0].click();", close_1)
    except:
        pass

    try:
        input_amount = await driver.find_element(By.XPATH, '//*[@id="send"]', timeout=20)
        await input_amount.write('18')

        pay_but = await driver.find_element(By.XPATH, '//*[@id="app"]/buy-gomining/section/card/div/div[1]/buy-token-crypto/card-token-buy/card/div/div[2]/div/div[2]/button', timeout=20)
        await asyncio.sleep(1.5)
        await driver.execute_script("arguments[0].click();", pay_but)

        pay_but_2 = await driver.find_element(By.XPATH, '//*[@id="html"]/body/modal-container/div[2]/div/modal-token-buy-confirm/modal/div/div[4]/div/div/div[2]/button', timeout=20)
        await asyncio.sleep(1)
        await driver.execute_script("arguments[0].click();", pay_but_2)
    except Exception as e:
        print(f'ERROR PAY BUT \n{e}')

    await asyncio.sleep(3.5)

    handles = await driver.window_handles
    print(handles)
    for handle in handles:
        await driver.switch_to.window(handle)
        title = await driver.title
        if "Pay" in title:
            break

    try:
        choose_trc20 = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/div[3]/button[3]', timeout=30)
        await asyncio.sleep(1)
        await choose_trc20.click()
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/div[4]/div/div[2]/div[3]/div/div/span', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div/div/div/div/div[4]/div/div[2]/div[1]/div/span', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)