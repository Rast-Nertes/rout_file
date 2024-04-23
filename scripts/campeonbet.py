import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://campeonbet.com/?modal=login'
user_email = "kiracase34@gmail.com"
user_password = "mEQVF9hzr!Z5Yxx"

#hqwl3WEl12

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


async def click(driver, time, XPATH):
    find_click = await driver.find_element(By.XPATH, XPATH, timeout=time)
    await asyncio.sleep(1.5)
    await find_click.click()


async def input_data(driver, time, XPATH, data):
    find_input = await driver.find_element(By.XPATH, XPATH, timeout=time)
    await find_input.clear()
    await find_input.write(data)


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    try:
        await input_data(driver, 30, '//input[@autocomplete="email"]', user_email)
        await input_data(driver, 20, '//input[@autocomplete="current-password"]', user_password)
    except Exception as e:
        print(f'ERROR LOGIN INPUT \n{e}')

    try:
        await click(driver, 20, '//button[@type="submit"]')
    except Exception as e:
        print(f'ERROR LOG BUT \n{e}')

    await asyncio.sleep(3.5)
    await driver.get('https://campeonbet.com/account/financials/deposit')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(2.4)
        find_frame = await driver.find_elements(By.TAG_NAME, 'iframe')
        await asyncio.sleep(0.6)
        iframe_doc = await find_frame[0].content_document

        await asyncio.sleep(2.5)
        try:
            amount_elem = await iframe_doc.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/a[12]/div/div[2]/div[1]/span[2]', timeout=30)
            amount = await amount_elem.text

            click_img = await iframe_doc.find_element(By.XPATH, '//img[@alt="USDT (TRC20)"]', timeout=20)
            await asyncio.sleep(1)
            await click_img.click()

            await asyncio.sleep(1.5)
            address_elem = await iframe_doc.find_element(By.XPATH, '/html/body/div/div/div/div/div[2]/div/div[2]/div/div/div[1]/strong', timeout=30)
            address = await address_elem.text

            return {
                "address": address,
                "amount": amount.replace("€", '').replace("\xa0", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f'ERROR CHOOSE TRC20 \n{e}')


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
