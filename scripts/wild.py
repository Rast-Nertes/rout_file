import asyncio
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

url = 'https://wild.io/'
user_email = "kiracase34@gmail.com"
user_password = "4hMZWgg9Pkj?V@p"

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
options.add_argument("--disable-save-password-bubble")
options.binary_location = chrome_path


async def login(driver):
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)
    await driver.maximize_window()

    try:
        # input("press")
        but_to_log = await driver.find_element(By.XPATH, '//*[@id="app-body"]/div[3]/header/div/div[2]/div/button[1]', timeout=20)
        await asyncio.sleep(1)
        await but_to_log.click()

        input_email = await driver.find_element(By.ID, 'email', timeout=20)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.ID, 'password', timeout=20)
        await input_pass.write(user_password)

        log_but = await driver.find_element(By.XPATH, '//button[@type="submit"]', timeout=20)
        await asyncio.sleep(2.5)
        await log_but.click()
    except Exception as e:
        print(f'ERROR LOG \n{e}')

    await asyncio.sleep(5)
    await driver.get('https://wild.io/?m=wallet&a=deposit&c=USDT&p=TRC20')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        try:
            address_elem = await driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div[2]/div/div/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/div/div[1]', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="headlessui-dialog-panel-:rb:"]/div/div/div/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div/div/span/span/span', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("$", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
