import asyncio
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

url = 'https://fortunejack.com/?loginRedirectTo=/verify'
user_email = "kiracase34@gmail.com"
user_password = "2BD.!aCMqj7U4tf"

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
options.add_argument("--disable-save-password-bubble")
options.binary_location = chrome_path
# options.add_extension(ext)


async def login(driver):
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)
    await driver.maximize_window()

    try:

        await asyncio.sleep(2)
        input_email = await driver.find_element(By.XPATH, '//input[@name="email"]', timeout=20)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.XPATH, '//input[@name="password"]', timeout=20)
        await input_pass.write(user_password)

        log_but = await driver.find_element(By.XPATH, '//button[@type="submit"]', timeout=20)
        await asyncio.sleep(2.5)
        await log_but.click()
    except Exception as e:
        print(f'ERROR LOG \n{e}')

    try:
        await asyncio.sleep(2.5)
        depos_button = await driver.find_element(By.XPATH, '//*[@id="header"]/div/div[2]/div/div[1]/button', timeout=20)
        await asyncio.sleep(1)
        await depos_button.click()
    except Exception as e:
        print(f'ERROR CLICK BUTTON \n{e}')

    try:
        choose_wal = await driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/div/div', timeout=20)
        await asyncio.sleep(1)
        await choose_wal.click()

        choose_usdt= await driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/div[2]/div[2]/div/div/div[2]/div[1]/div[3]/div[2]/div[2]/li', timeout=20)
        await asyncio.sleep(1)
        await choose_usdt.click()

        choose_net = await driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div', timeout=20)
        await asyncio.sleep(1)
        await choose_net.click()

        choose_trc = await driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/div[2]/div[2]/div/div/div[2]/div[2]/div[3]/div/li[1]', timeout=20)
        await asyncio.sleep(1)
        await choose_trc.click()
    except Exception as e:
        print(f'error choose net \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/div[2]/div[2]/div/div/div[3]/div[2]/div[2]', timeout=30)
            address = await address_elem.text

            # amount_elem = await driver.find_element(By.XPATH, '/html/body/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div/div/span[1]', timeout=30)
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
