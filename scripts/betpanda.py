import asyncio
import pyautogui
from anticaptchaofficial.imagecaptcha import *
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://betpanda.io/en/?type=login&modal=user'
user_email = "kiracase34@gmail.com"
user_password = "uE5FLwPj!mfjK6e"

# CHROME CONSTANTS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('../../../today_scripts/config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key_solver = paths[5].strip()
    api_anti = paths[2].strip()
    ext = paths[4].strip()

options.binary_location = chrome_path
options.add_extension(ext)


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

    await driver.get(url, timeout=60)

    try:
        await asyncio.sleep(2.4)
        find_frame = await driver.find_elements(By.TAG_NAME, 'iframe')
        await asyncio.sleep(0.6)
        iframe_doc = await find_frame[0].content_document
        click_checkbox = await iframe_doc.find_element(By.XPATH, '//*[@id="challenge-stage"]/div/label/input', timeout=20)
        await click_checkbox.click()
    except Exception as e:
        print(f'ERROR CHECKBOX \n{e}')

    try:
        await input_data(driver, 30, '//input[@name="email"]', user_email)
        await input_data(driver, 30, '//input[@name="password"]', user_password)
        await click(driver, 30, '/html/body/div[4]/div/div/div/div/div[2]/form/button')
        await click(driver, 5, '/html/body/div[4]/div/div/div/div/div[2]/form/button')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        await click(driver, 30, '//*[@id="currency-selector-button"]')
        await click(driver, 30, '//*[@id="currencyDropdown"]/div/div[1]/div[5]/div')
        await click(driver, 30, '//a[@class="btn btn-cta small top-deposit"]')
        await click(driver, 30, '/html/body/div[6]/div/div/div[2]/div[2]/div/div/div/div/div[2]/div[2]/div/div[2]/div')
    except Exception as e:
        return {"status": "0", "ext": f"ERROR CHOOSE TRC20 \n{e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="cryptoAddress"]', timeout=30)
            address = await address_elem.text
            #
            # amount_elem = await driver.find_element(By.XPATH, '//*[@id="auth"]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]', timeout=30)
            # amount = await amount_elem.text

            return {
                "address": address,
                "amount": "0.01",
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
