import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://ororo.tv/ru'
user_login = 'kiracase34@gmail.com'
user_password = 'kiraoleg6'

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
        find_error = await driver.find_element(By.XPATH, '//*[@id="main-message"]/h1/span', timeout=10)
        if find_error:
            await driver.refresh()
        print(f'ERROR PAGE')
    except Exception as e:
        pass

    try:
        await click(driver, 40, '//*[@id="wrapper"]/div[1]/header/div/div/nav/div[3]/ul/li[1]/a')
        await input_data(driver, 20, '//*[@id="user_email"]', user_login)
        await input_data(driver, 20, '//*[@id="user_password"]', user_password)
        await click(driver, 30, '//*[@id="new_user"]/input[2]')
    except Exception as e:
        print(f'ERROR INPUT LOG DATA \n{e}')

    await asyncio.sleep(10.5)
    await driver.get('https://ororo.tv/ru/users/subscription')

    try:
        await click(driver, 30, '//*[@id="payment-form"]/div[1]/label[1]/div/div/div[4]/div')
    except Exception as e:
        find_input_tag = driver.find_element(By.XPATH, '//*[@id="user_email"]')
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"ERROR DEPOS BUT \n{e}")

    try:
        await click(driver, 30, '//*[@id="payment-form"]/div[2]/div[2]/ul/li[2]/button')
    except Exception as e:
        print(f'ERROR CHOOSE CRYPTO \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        try:
            await click(driver, 30, '//img[@alt="Tether"]')
            await click(driver, 30, '//img[@alt="Tether TRC-20"]')
        except Exception as e:
            print(f'ERROR CHOOSE TETHER \n{e}')

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.CLASS_NAME, 'step-pay__address', timeout=50)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="step_pay__amount_payTo"]', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("\n", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)


