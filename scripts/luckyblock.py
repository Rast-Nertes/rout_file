import asyncio
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

url = 'https://www.luckyblock.top/cs?clickId=fx_b42842_0d8177e02931d2f611f4559da51fa191_1&overlay=cashier&tab=deposit'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

# CHROME CONSTANS
#C:/Users/Acer/Desktop/py_scripts/result/ROUT_FILE/config.txt
with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.binary_location = chrome_path


async def login(driver):
    await driver.get(url, timeout=80)
    await driver.maximize_window()

    try:
        input_email = await driver.find_element(By.ID, 'login-form-input-email', timeout=20)
        await asyncio.sleep(0.5)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.ID, 'login-form-input-password', timeout=20)
        await asyncio.sleep(0.5)
        await input_pass.write(user_password)
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    try:
        log_but = await driver.find_element(By.ID, 'login-form-submit-button', timeout=20)
        await asyncio.sleep(1.5)
        await log_but.click()
    except Exception as e:
        print(f"ERROR LOG BUT \n{e}")

    try:
        data_but = await driver.find_element(By.XPATH,
                                             '//*[@id="root"]/div[6]/div[1]/div[2]/header/div/div/div[1]/div/button',
                                             timeout=20)
        await asyncio.sleep(1.5)
        await data_but.click()

        data_but = await driver.find_element(By.XPATH,
                                             '//*[@id="root"]/div[6]/div[1]/div[2]/header/div/div/div[1]/div/button',
                                             timeout=20)
        await asyncio.sleep(1.5)
        await data_but.click()
    except Exception as e:
        print(f'ERROR LOG BUT\n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        try:
            await asyncio.sleep(4.5)
            address_elem = await driver.find_element(By.ID, 'deposit-address', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '/html/body/div[8]/div[3]/div/div/div/div/div[2]/div/p', timeout=30)
            amount = await amount_elem.text
        except Exception as e:
            print(f'ERROR DATA \n{e}')

        amount = ''.join(char for char in amount if char.isdigit() or char == '.')

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
