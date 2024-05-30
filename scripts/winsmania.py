import asyncio
import pyautogui
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://winsmania.com/en-GB/login'
user_email = "kiracase34"
user_password = "pKVBLCi5f!3$h67"

# CHROME CONSTANTS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
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
    ext = paths[4].strip()

options.add_extension(ext)
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
        await click(driver, 30, '/html/body/div[4]/div[2]/div/mat-dialog-container/app-language-suggestion/div/div[1]/i')
        await input_data(driver, 50, '//input[@name="username"]', user_email)
        await input_data(driver, 50, '//input[@name="password"]', user_password)
        await click(driver, 30, '/html/body/app-root/app-singin/div/div[2]/div/div/form/app-action-button/button')
    except Exception as e:
        return {"status":"0", "ext":f"error login:  {e} "}

    await asyncio.sleep(4.5)
    await driver.get('https://winsmania.com/en-GB/home/account/manage-balance/deposit')

    try:
        await click(driver, 30, '/html/body/app-root/app-main/div[1]/div/app-account/div/div/app-manage-balance/div/div[2]/app-manage-balance-deposit/app-manage-balance-transact/div/div/div/div[1]/div[5]/div/div[1]')
        await click(driver, 30, '/html/body/app-root/app-main/div[1]/div/app-account/div/div/app-manage-balance/div/div[2]/app-manage-balance-deposit/app-manage-balance-transact/div/div/div/div[2]/div/div/form/app-action-button/button')
    except Exception as e:
        return {"status": "0", "ext":f"error path to address:  {e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        try:
            amount_elem = await driver.find_element(By.XPATH, '/html/body/app-root/app-main/div[1]/div/app-account/div/div/app-manage-balance/div/div[2]/app-manage-balance-deposit/app-manage-balance-transact/div/div/div/div[2]/div/div/form/div[1]/div[1]', timeout=30)
            amount = await amount_elem.text
        except Exception as e:
            return {"status":"0", "ext":f"error amount:  {e}"}

        try:
            find_frame = await driver.find_element(By.CSS_SELECTOR, 'app-payment > div > div.frame > iframe', timeout=20)
            await asyncio.sleep(2.5)
            iframe_doc = await find_frame.content_document
        except Exception as e:
            # input("pr")
            return {"status":"0", "ext":f"error frame:  {e}"}

        await asyncio.sleep(4.5)
        try:
            address_elem = await iframe_doc.find_element(By.XPATH, '//*[@id="copyText"]', timeout=30)
            address = await address_elem.get_attribute('value')

            return {
                "address": address,
                "amount": amount.replace("$", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data:  {e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
