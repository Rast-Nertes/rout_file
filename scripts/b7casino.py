import asyncio
import pyautogui
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://b7casino.io/'
user_email = "kiracase34@gmail.com"
user_password = "35i9JC5XSkzUBvK"

# CHROME CONSTANTS

# proxy_address = "45.130.254.133"
# proxy_login = 'K0nENe'
# proxy_password = 'uw7RQ3'
# proxy_port = 8000

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
    api_key_solver = paths[5].strip()
    ext = paths[1].strip()

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
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    try:
        await asyncio.sleep(7.5)
        await click(driver, 50, '//*[@id="container"]/nav/section/div[3]/button[2]')
        await input_data(driver, 30, '//input[@autocomplete="username"]', user_email)
        await input_data(driver, 30, '//input[@type="password"]', user_password)
        await asyncio.sleep(1.5)
        await click(driver, 30, '//button[@form="login"]')
    except Exception as e:
        return {"status":"0", "ext":f"error login {e}"}

    try:
        await asyncio.sleep(3)
        await click(driver, 30, '//button[@data-smartico-id="cashier"]')
        await click(driver, 30, '//button[@class="cashier-payment-methods-expand-btn"]')
        await click(driver, 30, '//img[@alt="Cryptocurrency"]')
    except Exception as e:
        return {"status": "0", "ext": f"error choose crypto method {e}"}

    try:
        await click(driver, 30, '(//input[@class="has-value"])[1]')
        await click(driver, 30, '/html/body/div[4]/ul/li[4]')
    except Exception as e:
        return {"status": "0", "ext": f"error TRC20  {e}"}

    try:
        await click(driver, 30, '//button[@class="m-button m-gradient-border m-button--success m-button--medium cashier-submit"]')
    except Exception as e:
        return {"status": "0", "ext": f"error depos but  {e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[1]/input', timeout=30)
            address = await address_elem.get_attribute('value')

            amount_elem = await driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]/p/span', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace("0", '', 1).replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
