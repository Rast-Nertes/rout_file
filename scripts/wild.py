import asyncio
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
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
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.binary_location = chrome_path
options.add_argument('--headless')
# options.add_extension(ext)


async def login(driver):
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)
    await driver.maximize_window()

    try:
        but_to_log = await driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[3]/div/header/div/div[2]/div/div/button[1]', timeout=20)
        await asyncio.sleep(1)
        await but_to_log.click()

        input_email = await driver.find_element(By.ID, 'email', timeout=20)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.ID, 'password', timeout=20)
        await input_pass.write(user_password)

        log_but = await driver.find_element(By.XPATH, '//*[@id="headlessui-dialog-panel-:r4:"]/div[2]/div[2]/div/form/div[2]/div[1]/button', timeout=20)
        await asyncio.sleep(2.5)
        await log_but.click()
    except Exception as e:
        print(f'ERROR LOG \n{e}')

    try:
        choose_wal = await driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[3]/div/header/div/div[2]/div/div[1]/div[2]/button', timeout=20)
        await asyncio.sleep(1.5)
        await choose_wal.click()
    except Exception as e:
        print(f'error choose wal \n{e}' )

    try:
        choose_sect = await driver.find_element(By.XPATH, '//*[@id="headlessui-combobox-button-:rh:"]', timeout=20)
        await asyncio.sleep(1.5)
        await choose_sect.click()

        choose_net = await driver.find_element(By.XPATH, '//*[@id="headlessui-combobox-option-:rk:"]', timeout=20)
        await asyncio.sleep(1.5)
        await choose_net.click()
    except Exception as e:
        print(f'error choose trc20 \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="headlessui-dialog-panel-:r9:"]/div[2]/div/div[2]/div[2]/div/div[4]/div[2]/div/div/div[1]/div/div/div[1]/p[2]', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="headlessui-dialog-panel-:r9:"]/div[2]/div/div[2]/div[2]/div/div[4]/div[2]/div/div/div[2]/span[1]/span[1]', timeout=30)
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
