import asyncio
import pyautogui
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://join.czechvrnetwork.com/signup/signup.php?step=signup&nats=MC4wLjEzLjE0LjAuMC4wLjAuMA&switched=1&strack=0&#ucet'
user_email = "rwork875@gmail.com"
user_name = "rwork875"
user_password = "00001111Rw"

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
    ext = paths[4].strip()

# options.add_extension(ext)
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
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    try:
        await click(driver, 50, '(//div[@class="joinnow"])[1]')
        await click(driver, 30, '//*[@id="PayBitcoin"]')
        await input_data(driver, 30, '//*[@id="user"]', user_name)
        await input_data(driver, 30, '//*[@id="Pswd"]', user_password)
        await input_data(driver, 30, '//*[@id="mail"]', user_email)
        await click(driver, 10, '//*[@id="Bitcoin"]')
    except Exception as e:
        print(f'ERROR CHOOSE TARIFF \n{e}')

    await asyncio.sleep(5)
    await driver.clear_proxy()
    await asyncio.sleep(2)
    await driver.refresh()

    try:
        await js_click(driver, 40, '//img[@alt="USDT"]')
        await click(driver, 10, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/button')
        await click(driver, 30, '//img[@alt="Tron"]')
        await click(driver, 10, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div[2]/div/button')
    except Exception as e:
        print(f'error choose trc20 \n{e}')

    try:
        await input_data(driver, 30, '//input[@name="email"]', "kiracase34@gmail.com")
        await asyncio.sleep(1.5)
        await click(driver, 10, '//*[@id="__next"]/div/div/div[2]/div[1]/div[2]/button')
    except Exception as e:
        print(f'ERROR INPUT EMAIL \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[6]/div/div[2]/div', timeout=40)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div', timeout=20)
            amount = await amount_elem.text

            return {
                "address": address.replace("\n", '').replace("Copy", '').replace(" ", ''),
                "amount": amount.replace("USDT", '').replace("\n", '').replace("Copy", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
