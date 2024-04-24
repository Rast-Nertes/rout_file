import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://solisbet.com/en/'
user_email = "kiracase34"
user_password = "yDf-VmU3q-5@T5"

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

    try:
        await click(driver, 20, '/html/body/div[1]/div/nav/div/div[2]/div/button[1]')
    except Exception as e:
        print(f'ERROR SIGN IN BUTTON \n{e}')

    try:
        await input_data(driver, 20, '//*[@id="UserName"]', user_email)
        await input_data(driver, 20, '//*[@id="Password"]', user_password)
        await click(driver, 20, '/html/body/div[3]/div/div/section/div/div[1]/form/button')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        await asyncio.sleep(2.5)
        await click(driver, 20, '/html/body/div[1]/div/nav/div/div[2]/div/button/span')
    except Exception as e:
        find_input_tag = await driver.find_element(By.XPATH, '//*[@id="UserName"]', timeout=10)
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"ERROR DEPOS BUT \n{e}")

    try:
        await asyncio.sleep(1.5)
        await click(driver, 20, '/html/body/div[3]/div/div/div/div[2]/div[2]/div/div[1]/div[1]/div/div[1]/label[7]/span[2]')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div[1]/span', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[2]/div/div[1]/div[1]/div/div[2]/div[2]/div/div[2]/div[2]/div[1]', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": str(int(amount.replace("$", '').replace(" ", '')) + 0.01),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
