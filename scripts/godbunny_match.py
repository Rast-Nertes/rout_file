import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://godbunny.com/en/login'
user_email = "kiracase34@gmail.com"
user_password = "Kiramira123"

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
    await driver.get(url, timeout=100)

    try:
        await input_data(driver, 30, '//*[@id="email"]', user_email)
        await input_data(driver, 30, '//*[@id="password"]', user_password)
        await asyncio.sleep(1.5)
        await click(driver, 30, '//button[@data-wlc-element="button_login-submit"]')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    await asyncio.sleep(2.5)
    await driver.get('https://godbunny.com/en/profile/cash')

    try:
        await click(driver, 30, '//img[@alt="Praxis Match2Pay"]')
        await asyncio.sleep(1.5)
        await click(driver, 30, "//span[text()=' +20 ']")
    except Exception as e:
        find_input_tag = await driver.find_element(By.XPATH, '//*[@id="email"]', timeout=10)
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"ERROR CHOOSE MATCH BUT \n{e}")

    try:
        await asyncio.sleep(2)
        await click(driver, 30, '(//span[@class="wlc-btn__text"])[9]')
    except Exception as e:
        print(f'ERROR DEPOSIT BUT \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(7.4)
        find_frame = await driver.find_element(By.NAME, 'deposit_frame', timeout=90)
        await asyncio.sleep(0.6)
        iframe_doc = await find_frame.content_document

        try:
            click_select = await iframe_doc.find_element(By.XPATH, '//div[@class="custom-select-dropdown-arrow-container"]', timeout=60)
            await asyncio.sleep(1.5)
            await click_select.click()

            click_choosetrc20 = await iframe_doc.find_element(By.XPATH, "//div[text()='USX (USDT TRC20)']", timeout=30)
            await asyncio.sleep(1.5)
            await click_choosetrc20.click()
        except Exception as e:
            print(f'ERROR CHOOSE TRC20 \n{e}')

        try:
            depos_but = await iframe_doc.find_element(By.XPATH, "//button[text()='Deposit']", timeout=30)
            await asyncio.sleep(1.5)
            await depos_but.click()
        except Exception as e:
            print(f'ERROR DEPOS BUT CLICK \n{e}')

        await asyncio.sleep(10.5)
        find_frame = await driver.find_element(By.NAME, 'deposit_frame', timeout=90)
        await asyncio.sleep(0.5)
        iframe_doc = await find_frame.content_document

        await asyncio.sleep(2.5)
        try:
            amount_elem = await iframe_doc.find_element(By.XPATH, '(//strong)[1]', timeout=30)
            amount = await amount_elem.text

            address_elem = await iframe_doc.find_element(By.XPATH, '//span[@class="text"]', timeout=30)
            address = await address_elem.text

            return {
                "address": address,
                "amount": amount.replace("USD", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
