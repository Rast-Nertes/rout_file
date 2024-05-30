import asyncio
import pyautogui
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'http://1gocasino13.com'
user_email = "kiracase34@gmail.com"
user_password = "aHDqa22K2Z2xNGc"

# CHROME CONSTANTS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

options = webdriver.ChromeOptions()
options.add_argument("--disable-save-password-bubble")
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-notifications')
options.add_argument('--log-level=3')
options.add_argument('--disable-remote-fonts')

prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    api_key_solver = paths[5].strip()
    ext = paths[1].strip()

options.binary_location = chrome_path
options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})


async def js_click(driver, time, XPATH):
    find_click = await driver.find_element(By.XPATH, XPATH, timeout=time)
    await asyncio.sleep(1.5)
    await driver.execute_script("arguments[0].click();", find_click)


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
    await driver.get(url, timeout=120)

    try:
        await click(driver, 50, '//a[@data-test="dt-signin"]')
        await input_data(driver, 30, '//*[@id="email"]', user_email)
        await input_data(driver, 30, '//*[@id="password"]', user_password)
        await click(driver, 30, '//button[@data-test="auth-form-btn"]')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        await asyncio.sleep(8.5)
        await click(driver, 60, '//*[@id="app"]/div[6]/div/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div/div[2]/div/div[6]/div[1]')
        await asyncio.sleep(4)
        await click(driver, 30, '//*[@id="app"]/div[6]/div/div/div/div/div/div[2]/div[1]/div/div/div[4]/div[1]/div/div[2]/div[3]')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//div[@class="payment-crypto__wallet-address"]', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//p[@class="payment-crypto__text-sum"]', timeout=30)
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
