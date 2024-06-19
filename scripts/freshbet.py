import asyncio
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

url = 'https://freshbet.com/en/account/deposit'
user_email = "kiracase34"
user_password = "Rwuy!C.Wp.sPG8!"


# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    ext = paths[1].strip()
    
proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

options = webdriver.ChromeOptions()
options.binary_location = chrome_path
options.add_argument("--disable-save-password-bubble")


async def login(driver):
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await driver.get(url, timeout=60)
    await driver.maximize_window()

    try:
        await asyncio.sleep(2)
        input_email = await driver.find_element(By.XPATH, '/html/body/div[1]/form/ul/li[1]/input', timeout=20)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.XPATH, '/html/body/div[1]/form/ul/li[2]/input', timeout=20)
        await input_pass.write(user_password)

        log_but = await driver.find_element(By.XPATH, '/html/body/div[1]/form/ul/li[3]/button', timeout=20)
        await asyncio.sleep(2.5)
        await log_but.click()
    except Exception as e:
        print(f'ERROR LOG \n{e}')

    try:
        await asyncio.sleep(15)
        choose_tet = await driver.find_element(By.XPATH, '//li[@payment-method="tether usd "]', timeout=20)
        await choose_tet.click()

        choose_net = await driver.find_element(By.XPATH, '(//div[@class="network-select"]/div/div)[1]', timeout=20)
        await asyncio.sleep(1)
        await choose_net.click()

        choose_trc = await driver.find_element(By.XPATH, '((//div[@class="network-select"]/div/div)[2]/div)[2]', timeout=20)
        await asyncio.sleep(1)
        await choose_trc.click()
    except Exception as e:
        print(f'error choose net \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(2.5)
        try:
            await asyncio.sleep(2.5)
            address_elem = await driver.find_element(By.CSS_SELECTOR, 'li.crypto-payment-container > div > div.options > div.crypto-cont-el.visible > div > div', timeout=30)
            address = await address_elem.text

            return {
                "address": address,
                "amount": "0.01",
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
