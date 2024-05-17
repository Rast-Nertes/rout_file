import asyncio
import pyautogui
from anticaptchaofficial.imagecaptcha import *
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://www.fatbossonline.com/de/login-modal/'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123KK"


# CHROME CONSTANTS

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

options = webdriver.ChromeOptions()
# user_agent = UserAgent()
# options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    ext = paths[1].strip()

# options.add_extension(ext)
options.binary_location = chrome_path


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
        await click(driver, 60, '//*[@id="side-menu"]/div/div[2]/div/span[2]/a')
        await asyncio.sleep(3.5)
        await input_data(driver, 60, '//*[@id="login-modal"]/div/div/div[2]/div/form/div[1]/input', user_email)
        await input_data(driver, 30, '//*[@id="login-modal"]/div/div/div[2]/div/form/div[3]/input', user_password)
        await click(driver, 30, '//*[@id="login-modal"]/div/div/div[2]/div/form/button')
    except Exception as e:
        return {"status":"0", "ext":f"error login \n{e}"}

    await asyncio.sleep(4.5)
    await driver.get('https://www.fatbossonline.com/de/deposit-modal/')

    try:
        await click(driver, 60, '//*[@id="deposit-modal"]/div/div/div[2]/div/div/div/div/div[2]/span')
        await click(driver, 30, '//*[@id="deposit-modal"]/div/div/div[2]/div/div/div/div/div[1]/div[7]')
    except Exception as e:
        return {"status":"0", "ext":f"error choose trc20 \n{e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        amount_elem = await driver.find_element(By.XPATH, '//*[@id="deposit-modal"]/div/div/div[2]/div/div/form/div[1]/button[1]', timeout=30)
        amount = await amount_elem.text
        print(amount)

        await click(driver, 45, '//*[@id="deposit-modal"]/div/div/div[2]/div/div/form/div[1]/button[1]')
        await asyncio.sleep(2)
        await click(driver, 30, '//*[@id="deposit-modal"]/div/div/div[2]/div/div/form/div[3]/button')

        try:
            await asyncio.sleep(6.4)
            find_frame = await driver.find_elements(By.XPATH, '//*[@id="deposit-modal"]/div/div/div[2]/div/div/iframe')
            await asyncio.sleep(0.6)
            iframe_doc = await find_frame[0].content_document

            address_elem = await iframe_doc.find_element(By.XPATH, '/html/body/div/div/div/div/div/div/div/div[3]/img', timeout=30)
            src = await address_elem.get_attribute('src')
            await asyncio.sleep(4.5)
            address = src.split('trc20')[1].split("&")[0]

            return {
                "address": address.replace(":", ""),
                "amount": amount.replace("\xa0", '').replace("€", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data \n{e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
