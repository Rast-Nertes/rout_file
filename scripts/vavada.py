import asyncio
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://vavadaiyi.com/ru/login'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

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

options.binary_location = chrome_path


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    while True:
        try:
            await driver.find_element(By.XPATH, '//*[@id="_username"]', timeout=7.5)
            break
        except Exception:
            print("Refresh page")
            await driver.refresh()

    try:
        input_email = await driver.find_element(By.XPATH, '//*[@id="_username"]', timeout=50)
        await asyncio.sleep(0.5)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.XPATH, '//*[@id="_password"]', timeout=20)
        await asyncio.sleep(0.5)
        await input_pass.write(user_password)
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    try:
        click_log = await driver.find_element(By.XPATH, '//*[@id="_submit"]', timeout=20)
        await asyncio.sleep(0.5)
        await click_log.click()
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    await asyncio.sleep(2.5)
    await driver.get('https://vavadaiyi.com/en/profile/deposit/form/tether_trc20')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        while True:
            try:
                await driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div/fieldset[1]/div[2]/input', timeout=7.5)
                break
            except:
                print('refresh')
                await asyncio.sleep(2.5)
                await driver.get('https://vavadaiyi.com/en/profile/deposit/form/tether_trc20')

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div/fieldset[1]/div[2]/input', timeout=30)
            address = await address_elem.get_attribute('value')

            amount_elem = await driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div/div/fieldset[1]/p[3]', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("Minimum deposit is", '').replace("$", '').replace(" ", '') + "00",
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)