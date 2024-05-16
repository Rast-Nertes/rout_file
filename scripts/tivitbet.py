import asyncio
import pyautogui
from anticaptchaofficial.imagecaptcha import *
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://tivitbet.app/'
user_email = "kiracase34@gmail.com"
user_password = "Cjpq6Sxqm93imiF"


# CHROME CONSTANTS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

options = webdriver.ChromeOptions()
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
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
        await click(driver, 60, '//*[@id="root"]/div/div[4]/div/div[2]/div[2]/div/button[1]')
        await input_data(driver, 30, '//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/form/div[1]/div/input', user_email)
        await input_data(driver, 30, '//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/form/div[2]/div[1]/input', user_password)
        await asyncio.sleep(1.5)
        await click(driver, 30, '//*[@id="root"]/div/div[2]/div/div/div/div/div[2]/form/button')
    except Exception as e:
        return {"status": "0", "ext": f"login error \n{e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log
        try:
            await asyncio.sleep(3.5)
            await click(driver, 30, '//*[@id="root"]/div/div[4]/div/div[2]/div[2]/div/button')
            find_frame = await driver.find_element(By.XPATH, '//*[@id="billing-wrapper"]/iframe', timeout=20)
            await driver.switch_to.frame(find_frame)
            await asyncio.sleep(4)
            await click(driver, 30, '//*[@id="billing-widget-wrapper"]/div/div[3]/div[2]/div/div[2]/div[2]/button[1]')
            await click(driver, 30, '//*[@id="billing-widget-wrapper"]/div/div[3]/div[2]/div/button')

            await asyncio.sleep(5)
            address_elem = await driver.find_element(By.XPATH, '//*[@id="billing-widget-wrapper"]/div/div[3]/div[3]/button/span[1]', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="billing-widget-wrapper"]/div/div[3]/p[1]/span', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("₮", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
