import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://kent.casino/en/login'
user_email = "kiracase34@gmail.com"
user_password = "SyKvNd69QuSn7m9"

# CHROME CONSTANTS

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

options = webdriver.ChromeOptions()
options.add_argument("--disable-save-password-bubble")

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
    await driver.get(url, timeout=90)

    try:
        await asyncio.sleep(4.5)
        find_frame = await driver.find_elements(By.XPATH, '//*[@id="ts"]/iframe')
        await asyncio.sleep(0.5)
        iframe_doc = await find_frame[0].content_document
        click_checkbox = await iframe_doc.find_element(By.XPATH, '//*[@id="challenge-stage"]/div/label/input', timeout=20)
        await click_checkbox.click()
    except Exception as e:
        print(f'ERROR CHECKBOX \n{e}')

    try:
        await asyncio.sleep(2.5)
        await input_data(driver, 30, '//*[@id="email"]', user_email)
        await input_data(driver, 30, '//*[@id="password"]', user_password)
        await click(driver, 30, '//button[@type="submit"]')
    except Exception as e:
        return {"status":"0", "ext":f"error login {e}"}

    await asyncio.sleep(5)
    await driver.get('https://kent.casino/en/profile/cash', timeout=90)

    try:
        await click(driver, 30, '//img[@alt="USDT TRC-20"]')
    except Exception as e:
        return {"status":"0", "ext":f"error choose trc20 {e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '/html/body/div[1]/div/div[8]/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/div/button', timeout=30)
            await address_elem.click()

            await asyncio.sleep(2.5)
            address = pyperclip.paste()

            amount_elem = await driver.find_element(By.XPATH, '/html/body/div[1]/div/div[8]/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div[3]/span[1]', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("€", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data{e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
