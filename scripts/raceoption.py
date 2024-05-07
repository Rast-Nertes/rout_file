import asyncio
import pyautogui
from twocaptcha import TwoCaptcha
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://raceoption.com/en/login'
user_email = "kejokan542@haislot.com"
user_password = "Qwerty17"

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
    api_anti = paths[2].strip()
    api_key_solver = paths[5].strip()
    ext = paths[4].strip()

options.binary_location = chrome_path
options.add_extension(ext)


async def api_connect():
    await asyncio.sleep(0.4)
    pyautogui.moveTo(1730, 75)
    pyautogui.click()

    await asyncio.sleep(1)

    for _ in range(2):
        pyautogui.press('down')
        await asyncio.sleep(0.15)
    pyautogui.press('enter')

    await asyncio.sleep(1.5)

    for _ in range(4):
        pyautogui.press('tab')
        await asyncio.sleep(0.15)

    await asyncio.sleep(3.5)
    pyautogui.typewrite(api_key_solver, 0.1)
    await asyncio.sleep(1.5)

    pyautogui.moveTo(1730, 15)
    pyautogui.click()
    await asyncio.sleep(2)


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

    await api_connect()

    await asyncio.sleep(2.5)
    await driver.get(url, timeout=60)
    await asyncio.sleep(2.5)
    await driver.refresh()

    try:
        await input_data(driver, 30, '//*[@id="email"]', user_email)
        await asyncio.sleep(3.5)
        await input_data(driver, 30, '//*[@id="pass"]', user_password)
        await asyncio.sleep(3.5)
        await click(driver, 30, '/html/body/div[1]/main/section/div/div/div/div[2]/div[2]/form/div[3]/div[2]/button')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')
        return "Error login"
    
    await driver.get('https://raceoption.com/trading/deposit')
    await asyncio.sleep(3.5)
    await driver.refresh()

    await asyncio.sleep(2.5)
    try:
        await click(driver, 30, '//div[@class="pay-method ng-star-inserted" and contains(text(), "Криптовалюты")]')
    except Exception as e:
        return f'ERROR CHOOSE CRYPTOPAY \n{e}'

    try:
        await asyncio.sleep(1)
        await click(driver, 30, '//li[@class="crypto-list-item ng-star-inserted" and contains(text(), "Tether (USDT) TRC-20")]')
        await asyncio.sleep(1)
        await click(driver, 30, '/html/body/app-root/app-account-funding/div/div/app-deposit-amount/ul/li[1]/button')
    except Exception as e:
        print(f'ERORR CLICKs \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            amount_elem = await driver.find_element(By.XPATH, '//*[@id="app-scroll"]/app-crypto-deposit-info/div/div/div[2]/app-copy-button/div/span', timeout=30)
            amount = await amount_elem.text

            address_elem = await driver.find_element(By.XPATH, '//*[@id="app-scroll"]/app-crypto-deposit-info/div/div/div[3]/div[2]/app-copy-button/div/span', timeout=30)
            address = await address_elem.text

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
