import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://superboss222.com/ru-ua/login'
user_email = "kiracase34@gmail.com"
user_password = "Kiramira123"

#hqwl3WEl12

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
    # await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=90)

    try:
        await input_data(driver, 30, '//input[@autocomplete="username"]', user_email)
        await input_data(driver, 20, '//input[@name="password"]', user_password)
        await asyncio.sleep(1.5)
        await click(driver, 30, '//button[@type="submit"]')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    await asyncio.sleep(6)
    await driver.get('https://superboss222.com/en-eu/cabinet/cashier/deposit')

    try:
        await click(driver, 50, '//*[@id="__next"]/div[3]/div/div/div/div/div/div/div[2]/div/div/div/div[1]/div[1]/div/div/div[2]/div[2]/div[5]/div[2]/div[3]/div/div')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    # input("press")

    try:
        await asyncio.sleep(12.5)
        find_cont_but = await driver.find_element(By.XPATH, '//*[@id="amount"]/div/div[2]/button', timeout=50)
        await asyncio.sleep(2.5)
        await find_cont_but.click()
    except Exception as e:
        print(f'ERROR CLICK CONT \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="__next"]/div[3]/div/div/div/div/div/div/div[2]/div/div/div/div/div/div[3]/div/div[2]/div[1]/div[2]', timeout=30)
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
