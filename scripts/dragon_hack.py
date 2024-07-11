import asyncio
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://dragon-hack.pro/product/dota-2-melonity/'
user_email = "kiracase34@gmail.com"
user_password = "Kiramira123!"

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
        a_href = await driver.find_element(By.XPATH, '/html/body/div[1]/main/section/div/div/div[4]/aside/div[1]/div[5]/a', timeout=20)
        href = await a_href.get_attribute('href')
        await driver.get(href)

        await click(driver, 30, '//*[@id="btn_next"]')
    except Exception as e:
        print(f'ERROR HREF \n{e}')

    try:
        await asyncio.sleep(5)
        choose_click = await driver.find_element(By.XPATH, '//*[@id="TypeCurr_msdd"]', timeout=35)
        await asyncio.sleep(1.5)
        await choose_click.click()

        choose_trc20 = await driver.find_element(By.XPATH, '//span[@class="ddlabel" and text()="USDT"]', timeout=20)
        await asyncio.sleep(1.5)
        await choose_trc20.click()
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    try:
        await input_data(driver, 30, '//*[@id="email"]', user_email)
        await input_data(driver, 30, '//*[@id="Re_Enter_Email"]', user_email)
        await click(driver, 30, '//*[@id="pay_btn"]')
    except Exception as e:
        print(f'ERROR PLACE ORDER \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            amount_elem = await driver.find_element(By.XPATH, '//*[@id="form1"]/section/section/div[2]/div[2]/div[4]/p/span', timeout=30)
            amount = await amount_elem.text

            address_elem = await driver.find_element(By.XPATH, '//*[@id="form1"]/section/section/div[2]/div[2]/div[4]/div/div[1]/div/span', timeout=30)
            address = await address_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)