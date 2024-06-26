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
    await asyncio.sleep(2)
    await driver.get(url, timeout=60)

    try:
        await click(driver, 60, '//*[@id="root"]/div/div[4]/div/div[2]/div[2]/div/button[1]')
        await input_data(driver, 30, '//input[@name="username"]', user_email)
        await input_data(driver, 30, '//input[@name="password"]', user_password)
        await asyncio.sleep(1.5)
        await click(driver, 30, '//button[@type="submit"]')
    except Exception as e:
        return {"status": "0", "ext": f"login error \n{e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        try:
            await asyncio.sleep(3.5)

            try:
                await click(driver, 30, '//*[@id="root"]/div/div[4]/div/div[2]/div[2]/div/button')
            except Exception as e:
                return {"status": "0", "ext": f"depos but error \n{e}"}

            await asyncio.sleep(6.4)
            find_frame = await driver.find_elements(By.XPATH, '//*[@id="billing-wrapper"]/iframe')
            await asyncio.sleep(0.6)
            iframe_doc = await find_frame[0].content_document

            click_min_amoun = await iframe_doc.find_element(By.XPATH, '//*[@id="billing-widget-wrapper"]/div/div[3]/div[2]/div/div[2]/div[2]/button[1]', timeout=10)
            await asyncio.sleep(1.5)
            await click_min_amoun.click()

            click_depos_but = await iframe_doc.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div[2]/div/button')
            await asyncio.sleep(1.5)
            await click_depos_but.click()

            await asyncio.sleep(5)
            address_elem = await iframe_doc.find_element(By.XPATH, '/html/body/div/div/div/div[3]/div[3]/button/span[1]', timeout=30)
            address = await address_elem.text

            amount_elem = await iframe_doc.find_element(By.XPATH, '/html/body/div/div/div/div[3]/p[1]/span', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("₮", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status": "0", "ext": f"error data \n{e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
