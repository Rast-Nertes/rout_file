import asyncio
import pyautogui
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://777crypto.bet/'
user_email = "kiracase34@gmail.com"
user_password = "9fu.jsK@EU9zSiN"

# CHROME CONSTANTS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000
#
# proxy_address = "196.19.121.187"
# proxy_login = 'WyS1nY'
# proxy_password = '8suHN9'
# proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--disable-save-password-bubble")
options.add_argument('--log-level=3')
options.add_argument('--disable-remote-fonts')

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    api_key_solver = paths[5].strip()
    ext = paths[4].strip()

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
        await click(driver, 60, '/html/body/div[3]/div[1]/div/div/div/nav/div[2]/div/button[1]')
        await input_data(driver, 30, '//*[@id="email"]', user_email)
        await input_data(driver, 30, '//*[@id="password"]', user_password)
        await click(driver, 30, '//*[@id="form-login"]/div[3]/button')
    except Exception as e:
        return {"status":"0", "ext":f"error login \n{e}"}

    try:
        find_elem = await driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div/div/nav/div[2]/div/button', timeout=30)
        await asyncio.sleep(3.4)
        await click(driver, 30, '/html/body/div[3]/div[1]/div/div/div/nav/div[2]/div/button')
        await click(driver, 30, '//*[@id="wallet-modal-deposit-network-15-tab"]')
    except Exception as e:
        return {"status":"0", "ext":f"error path to log \n{e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(6.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[2]/div/div[1]/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[2]', timeout=20)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="wallet-modal-deposit-network-15"]/div[1]/div/div[1]/div[3]', timeout=20)
            amount = await amount_elem.text
            return {
                "address": address.replace("\n", '').replace(" ", ''),
                "amount": amount.replace("Min.", '').replace("Deposit:", '').replace("USDT", '').replace("\n", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
