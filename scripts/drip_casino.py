import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://drip.casino/'
user_email = "kiracase34@gmail.com"
user_password = "gzQH_T6qjWS*%MT"

#hqwl3WEl12

# CHROME CONSTANTS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()

options.binary_location = chrome_path


async def click(driver, time, XPATH):
    find_click = await driver.find_element(By.XPATH, XPATH, timeout=time)
    await asyncio.sleep(1.5)
    await find_click.click()


async def input_data(driver, time, XPATH, data):
    find_input = await driver.find_element(By.XPATH, XPATH, timeout=time)
    await find_input.clear()
    await find_input.write(data)


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    await asyncio.sleep(7.5)
    try:
        click_login_but = await driver.find_element(By.XPATH, '//*[@id="user-top__login-link"]', timeout=30)
        await asyncio.sleep(1.5)
        await driver.execute_script("arguments[0].click();", click_login_but)

        await input_data(driver, 30, '//*[@id="email"]', user_email)
        await input_data(driver, 30, '//*[@id="password"]', user_password)
        await click(driver, 20, '//*[@id="app"]/div[5]/div[1]/div/div/div/div[1]/div/div/div/div/div/div[2]/form/div[2]/button')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        await click(driver, 30, '//*[@id="app"]/header/div[2]/div[2]/div/div/a[2]')
        await click(driver, 30, '//*[@id="app"]/div[6]/div/div/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div/div/div[2]/div[6]')
    except Exception as e:
        find_input_tag = await driver.find_element(By.XPATH, '//*[@id="email"]', timeout=10)
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"ERROR DEPOS BUT \n{e}")

    try:
        await asyncio.sleep(3.5)
        await click(driver, 30, '//*[@id="app"]/div[6]/div/div/div/div/div/div[2]/div[1]/div/div/div[4]/div[1]/div/div[2]/div[3]')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.CLASS_NAME, 'payment-crypto__wallet-address', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.CLASS_NAME, 'payment-crypto__text-sum', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
