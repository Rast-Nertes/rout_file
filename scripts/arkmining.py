import asyncio
import pickle
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://arkmining.vip/signin'
user_email = "lasawo9725@rartg.com"
user_password = "Qwerty62982"

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
    api_ru = paths[3].strip()
    ext = paths[1].strip()

# options.add_extension(ext)
options.binary_location = chrome_path


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    # try:
    #     await asyncio.sleep(2.4)
    #     find_frame = await driver.find_elements(By.TAG_NAME, 'iframe')
    #     await asyncio.sleep(0.6)
    #     iframe_doc = await find_frame[0].content_document
    #     click_checkbox = await iframe_doc.find_element(By.XPATH, '//*[@id="challenge-stage"]/div/label/input', timeout=10)
    #     await click_checkbox.click()
    # except Exception as e:
    #     print(f'ERROR CHECKBOX \n{e}')

    try:
        input_user_log = await driver.find_element(By.XPATH, '//*[@id="email"]', timeout=50)
        await asyncio.sleep(1.5)
        await input_user_log.write(user_email)

        input_password = await driver.find_element(By.XPATH, '//*[@id="password"]', timeout=30)
        await asyncio.sleep(1)
        await input_password.write(user_password)
    except Exception as e:
        print(f'ERROR INPUT LOG DATA \n{e}')

    try:
        click_log = await driver.find_element(By.XPATH, '//button[@type="submit"]', timeout=20)
        await asyncio.sleep(1)
        await click_log.click()
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    await asyncio.sleep(2.5)
    await driver.get('https://arkmining.vip/deposit')

    try:
        click_select = await driver.find_element(By.XPATH, '//*[@id="network_input"]', timeout=30)
        await asyncio.sleep(1)
        await click_select.click()

        choose_trc20 = await driver.find_element(By.XPATH, '//div[@value="USDT-TRC20 [Network: Tron]"]', timeout=30)
        await asyncio.sleep(1)
        await choose_trc20.click()
    except Exception as e:
        print(f'ERROR SELECT \n{e}')

    try:
        input_amount = await driver.find_element(By.XPATH, '//*[@id="amount"]', timeout=20)
        await asyncio.sleep(1)
        await input_amount.write('200')
    except Exception as e:
        print(f'ERROR INPUT AMOUNT \n{e}')

    try:
        submit_but = await driver.find_element(By.XPATH, '//*[@id="edited_"]/a/button', timeout=30)
        await asyncio.sleep(1)
        await submit_but.click()
    except Exception as e:
        print(f'ERROR SUBMIT \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="deposit_preload"]/div/div/div/form/div/div[2]/input', timeout=30)
            address = await address_elem.__getattribute__('value')

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="deposit_preload"]/div/div/div/form/div/div[1]/input', timeout=30)
            amount = await amount_elem.__getattribute__('value')

            return {
                "address": address,
                "amount": amount.replace('USDT', '').replace(" ", ''),
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
