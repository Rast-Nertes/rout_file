import asyncio
import pyperclip
from twocaptcha import TwoCaptcha
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS


url = 'https://binomo.com/auth'
user_email = "kejokan542@haislot.com"
user_password = "Qwerty17."

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
    api_key = paths[3].strip()
    ext = paths[1].strip()

options.binary_location = chrome_path
# options.add_extension(ext)


async def click(driver, time, XPATH):
    find_click = await driver.find_element(By.XPATH, XPATH, timeout=time)
    await asyncio.sleep(1.5)
    await find_click.click()


async def input_data(driver, time, XPATH, data):
    find_input = await driver.find_element(By.XPATH, XPATH, timeout=time)
    await find_input.clear()
    await asyncio.sleep(0.5)
    await find_input.write(data)


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    try:
        await input_data(driver, 30, '//*[@id="qa_auth_LoginEmailInput"]/way-input/div/div/way-input-text/input', user_email)
        await input_data(driver, 30, '//*[@id="qa_auth_LoginPasswordInput"]/way-input/div/div/way-input-password/input', user_password)
        await click(driver, 30, '//*[@id="qa_auth_LoginBtn"]/button')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    await asyncio.sleep(2.5)
    await driver.get('https://binomo.com/trading/cashier/deposit/USDTT?amount=100000')

    try:
        await click(driver, 30, '/html/body/ng-component/vui-modal/div/div/div/ng-component/div[1]/div[3]/div/platform-ui-scroll/div/div/div/div/cashier-order/div/vui-button/button')
    except Exception as e:
        print(f'ERROR INPUT MIN AMOUNT \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            amount_elem = await driver.find_element(By.XPATH, '//div[@class="amount"]', timeout=30)
            amount = await amount_elem.text

            address_elem = await driver.find_element(By.XPATH, '//div[@class="address"]', timeout=30)
            address = await address_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDTT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
