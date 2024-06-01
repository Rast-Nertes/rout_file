import asyncio
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

url = 'https://www.cloudbet32.com/ru/auth/sign-in'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    ext = paths[1].strip()

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.binary_location = chrome_path
# options.add_extension(ext)


async def login(driver):
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await driver.get(url, timeout=60)
    await driver.maximize_window()

    try:
        input_email = await driver.find_element(By.XPATH, '//*[@id="signInEmail"]', timeout=20)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.XPATH, '//*[@id="signInPassword"]', timeout=20)
        await input_pass.write(user_password)

        click_log_but = await driver.find_element(By.XPATH, '(//button[@type="button"])[3]', timeout=20)
        await asyncio.sleep(2)
        await click_log_but.click()
    except Exception as e:
        return {"status":"0", "ext":f"error login {e}"}

    try:
        depos_click = await driver.find_element(By.CSS_SELECTOR, '#hud-wallet-desktop > button', timeout=20)
        await asyncio.sleep(1.5)
        await depos_click.click()

        choose_crypto = await driver.find_element(By.XPATH, '(//img[@alt="Cloudbet icon"])[7]', timeout=20)
        await asyncio.sleep(1.5)
        await choose_crypto.click()
    except Exception as e:
        return {"status":"0", "ext":f"error depos button {e}"}

    try:
        choose_coint = await driver.find_element(By.XPATH, '(//button[@data-test-crypto="USDT"])[1]', timeout=20)
        await asyncio.sleep(1)
        await choose_coint.click()

        choose_tet = await driver.find_element(By.XPATH, '(//button[@type="button"])[10]', timeout=20)
        await asyncio.sleep(1)
        await choose_tet.click()
    except Exception as e:
        return {"status":"0", "ext":f"error choose tether {e}"}

    try:
        choose_tron = await driver.find_element(By.XPATH, '//li[@data-test-network="tron"]', timeout=20)
        await asyncio.sleep(1)
        await choose_tron.click()
    except Exception as e:
        return {"status":"0", "ext":f"error choose net {e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(10.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="actionInput"]', timeout=30)
            address = await address_elem.get_attribute('value')

            return {
                "address": address,
                "amount": '0.01',
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
