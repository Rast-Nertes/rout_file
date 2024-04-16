import asyncio
import pyperclip
import pickle
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://gamblezen.com/'
user_email = "kiracase34@gmail.com"
user_password = ".VXs43T3S4LhyRq"

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
    await driver.get(url, timeout=60)

    try:
        log_but = await driver.find_element(By.XPATH, '//*[@id="headerSignInButton"]', timeout=45)
        await asyncio.sleep(1)
        await log_but.click()
    except Exception as e:
        print(f'ERROR LOG BUTTON \n{e}')

    try:
        input_email = await driver.find_element(By.XPATH, '//*[@id="login"]', timeout=20)
        await input_email.write(user_email)

        input_password = await driver.find_element(By.XPATH, '//*[@id="password"]', timeout=20)
        await input_password.write(user_password)

        login_button = await driver.find_element(By.XPATH, '//*[@id="popupSubmit"]', timeout=20)
        await asyncio.sleep(1)
        await login_button.click()
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        dpos_but = await driver.find_element(By.XPATH, '//*[@id="headerDepositButton"]', timeout=30)
        await asyncio.sleep(1)
        await dpos_but.click()
    except Exception as e:
        print(f'ERROR DEPOS BUTTON \n{e}')

    try:
        choose_trc20 = await driver.find_element(By.XPATH, '//*[@id="walletDepositPaymentList"]/div[3]/div/div[11]', timeout=30)
        await asyncio.sleep(1)
        await choose_trc20.click()
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    try:
        choose_25_amount = await driver.find_element(By.XPATH, '//*[@id="depositModal"]/div[2]/div/div/div/div/div/div[1]/div[2]/form/ul/li[1]', timeout=20)
        await asyncio.sleep(1)
        await choose_25_amount.click()

        depos = await driver.find_element(By.XPATH, '//*[@id="cashierDepositSubmit"]', timeout=20)
        await asyncio.sleep(1)
        await depos.click()
    except Exception as e:
        print(f'ERROR DEPOS \n{e}')

    try:
        copy = await driver.find_element(By.XPATH, '//*[@id="cryptoCopyButton"]', timeout=20)
        await asyncio.sleep(1)
        await copy.click()
    except Exception as e:
        print(f'ERROR COPY BUT \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(4.5)

        try:
            address = pyperclip.paste()

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="cryptoModal"]/div[2]/div/div/div[1]/p', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDTT", '').replace(" ", '').replace('\n', ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)


if __name__ == "__main__":
    wallet()
