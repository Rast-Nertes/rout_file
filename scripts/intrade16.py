import asyncio
import pyperclip
from twocaptcha import TwoCaptcha
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://intrade16.bar/login'
user_email = "rwork875@gmail.com"
user_password = "fPUmKyjuhUhe4"

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
    api_key = paths[3].strip()
    ext = paths[1].strip()

options.binary_location = chrome_path
# options.add_extension(ext)


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
        await click(driver, 30, '//a[@class="main-header__btn  btn  btn--black  p-open"]')
        await input_data(driver, 30, '//*[@id="input-log-in1"]', user_email)
        await input_data(driver, 30, '//*[@id="input-log-in2"]', user_password)
        await click(driver, 30, '//*[@id="log-in"]/form/button')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    await asyncio.sleep(5)
    await driver.get('https://intrade16.bar/pay')

    try:
        await click(driver, 30, '//*[@id="payment"]/div[1]/ul/li[2]/label')
        await click(driver, 30, '//*[@id="tron_checkbox"]')
        await click(driver, 30, '//*[@id="add_cash_4bill"]')
    except Exception as e:
        find_input_tag = await driver.find_element(By.XPATH, '//*[@id="input-log-in1"]', timeout=10)
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f'ERROR CHOOSE TRC20 \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(5.5)
        try:
            amount_elem = await driver.find_element(By.XPATH, '//*[@id="pay-global"]/div/div[5]/div[1]/div[3]/div[5]/span', timeout=30)
            amount = await amount_elem.text

            address_elem = await driver.find_element(By.XPATH, '//*[@id="pay-global"]/div/div[5]/div[1]/div[3]/div[7]/div[2]', timeout=30)
            address = await address_elem.text

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