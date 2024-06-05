import asyncio
import pyautogui
from flask import jsonify
from anticaptchaofficial.recaptchav3proxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

url = 'https://www.manyvids.com/Login/'
user_email = "rwork875@gmail.com"
user_password = "66447722r"

# CHROME CONSTANS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
# options.add_argument("--auto-open-devtools-for-tabs")
options.binary_location = chrome_path


async def login(driver):
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(2)
    # await driver.maximize_window()
    await driver.get(url, timeout=60)
    # input("oress")

    try:
        input_email = await driver.find_element(By.XPATH, '//input[@name="userName"]', timeout=20)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.XPATH, '//input[@name="password"]', timeout=20)
        await input_pass.write(user_password)
    except Exception as e:
        return {"status":"0", "ext":f"error input log data {e}"}

    try:
        log_button = await driver.find_element(By.XPATH, '//button[@type="submit"]', timeout=10)
        sleep(1.5)
        await driver.execute_script("arguments[0].click();", log_button)
    except Exception as e:
        return {"status":"0", "ext":f"error log button {e}"}

    await asyncio.sleep(7.5)
    await driver.get('https://www.manyvids.com/premium/upgrade/')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)
        try:
            choose_tariff = await driver.find_element(By.ID, 'plan-card_button_Subscribe-bottom-1month', timeout=30)
            await asyncio.sleep(2.5)
            await driver.execute_script("arguments[0].click();", choose_tariff)
        except Exception as e:
            return {"status":"0", "ext":f"error choose tariff{e}"}

        await asyncio.sleep(3)
        try:
            checkout = await driver.find_element(By.XPATH, '//*[@id="mvts-checkout-coingate-btn"]', timeout=20)
            await asyncio.sleep(2)
            await driver.execute_script("arguments[0].click();", checkout)
        except Exception as e:
            return {"status":"0", "ext":f"error checkout {e}"}

        await asyncio.sleep(7.5)
        await driver.clear_proxy()

        try:
            choose_tether = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div/label[8]', timeout=60)
            await asyncio.sleep(1.5)
            await driver.execute_script("arguments[0].click();", choose_tether)

            continue_button = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/button[1]', timeout=20)
            await asyncio.sleep(1.5)
            await driver.execute_script("arguments[0].click();", continue_button)
        except Exception as e:
            return {"status":"0", "ext":f"error choose tet {e}"}

        try:
            choose_tron = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[3]/div/div/label[3]', timeout=20)
            await asyncio.sleep(1.5)
            await choose_tron.click()

            continue_button_step_2 = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div[2]/div/button', timeout=20)
            await asyncio.sleep(1.5)
            await continue_button_step_2.click()
        except Exception as e:
            return {"status":"0", "ext":f"error choose tron{e}"}

        try:
            input_email = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[1]/form/div/div[2]/input', timeout=30)
            await input_email.click()
            await asyncio.sleep(2.5)
            pyautogui.typewrite(user_email)

            continue_button_2 = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[1]/div[2]/button', timeout=20)
            await driver.execute_script("arguments[0].removeAttribute('disabled')", continue_button_2)
            await asyncio.sleep(1.5)
            await continue_button_2.click()
        except Exception as e:
            return {"status":"0", "ext":f"error input data {e}"}

        try:
            amount_elem = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/p', timeout=30)
            amount = await amount_elem.text

            address_elem = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[6]/div/div[2]/div/p', timeout=20)
            address = await address_elem.text
            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)