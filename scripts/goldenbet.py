import asyncio
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

url = 'http://goldenbet.com'
user_email = "rwork875"
user_password = "3644Lem"
#3644Lem
#rwork22133

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
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.binary_location = chrome_path


async def login(driver):
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await driver.get(url, timeout=60)
    await driver.maximize_window()

    try:
        log_but = await driver.find_element(By.XPATH, '/html/body/header/div/div/ul/li[2]', timeout=20)
        await asyncio.sleep(1.5)
        await log_but.click()

        await asyncio.sleep(2)
        input_email = await driver.find_element(By.XPATH, '/html/body/div[2]/form/div/div[1]/input', timeout=20)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.XPATH, '/html/body/div[2]/form/div/div[2]/input', timeout=20)
        await input_pass.write(user_password)

        log_but = await driver.find_element(By.XPATH, '/html/body/div[2]/form/div/div[3]/button', timeout=20)
        await asyncio.sleep(2.5)
        await log_but.click()
    except Exception as e:
        print(f'ERROR LOG \n{e}')

    try:
        await asyncio.sleep(2.5)
        depos_button = await driver.find_element(By.XPATH, '/html/body/header/div/div/div[1]/div/ul/li[5]/a', timeout=20)
        await asyncio.sleep(1)
        await depos_button.click()
    except Exception as e:
        print(f'ERROR CLICK BUTTON \n{e}')

    try:
        # choose_wal = await driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/div/div', timeout=20)
        # await asyncio.sleep(1)
        # await choose_wal.click()

        choose_usdt= await driver.find_element(By.XPATH, '/html/body/main/div[3]/ul/li[4]/div[5]', timeout=20)
        await asyncio.sleep(1)
        await choose_usdt.click()

        choose_net = await driver.find_element(By.XPATH, '/html/body/main/div[3]/ul/li[5]/div/div[1]/div[1]/div/div[1]', timeout=20)
        await asyncio.sleep(1)
        await choose_net.click()

        choose_trc = await driver.find_element(By.XPATH, '/html/body/main/div[3]/ul/li[5]/div/div[1]/div[1]/div/div[2]/div[2]', timeout=20)
        await asyncio.sleep(1)
        await choose_trc.click()
    except Exception as e:
        print(f'error choose net \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '/html/body/main/div[3]/ul/li[5]/div/div[1]/div[2]/div/div', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '/html/body/main/div[3]/ul/li[4]/div[4]/p[1]/span[2]', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace('EUR', '').replace(" ", '') + ".00",
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
