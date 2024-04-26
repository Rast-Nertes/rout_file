import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://payertopay.ru/eftbuy'
user_email = "kiracase34@gmail.com"
user_password = "@iX9BWHv95nb7Pu"

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
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    try:
        await click(driver, 30, '/html/body/div/div[4]/div/div[2]/div/div/div/a/div/span')
    except Exception as e:
        print(f'ERROR PAY BUT \n{e}')

    try:
        await input_data(driver, 30, '//input[@name="Email"]', user_email)
        await click(driver, 30, '//button[@class="t-submit"]')
    except Exception as e:
        print(f'ERROR ACCEPT \n{e}')

    try:
        await click(driver, 30, '/html/body/div[3]/section/div/div[2]/div[2]/label[8]/span/img')
        await click(driver, 30, '/html/body/div[3]/section/div/div[2]/button')
    except Exception as e:
        print(f'ERROR CHOOSE CRYPTO \n{e}')

    try:
        await asyncio.sleep(12)
        await click(driver, 30, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[3]/button')
    except Exception as e:
        print(f'ERROR BUY BUT \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div/span', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/span', timeout=30)
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
