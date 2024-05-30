import asyncio
import pyautogui
from anticaptchaofficial.imagecaptcha import *
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://betplays.com/'
user_email = "kiracase34@gmail.com"
user_password = "R&L4_Fd9e.QBN2"

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
    api_key_solver = paths[5].strip()
    api_anti = paths[2].strip()
    ext = paths[4].strip()

options.binary_location = chrome_path
# options.add_extension(ext)


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
    await driver.get(url, timeout=120)

    try:
        await click(driver, 30, '//a[@automation="home_login_button"]')
        await input_data(driver, 30, '//*[@id="email"]', user_email)
        await input_data(driver, 30, '//*[@id="password"]', user_password)
        await click(driver, 30, '//*[@id="login_container"]/div/div[4]/button')
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    try:
        await asyncio.sleep(2.4)
        find_frame = await driver.find_elements(By.TAG_NAME, 'iframe')
        await asyncio.sleep(0.6)
        iframe_doc = await find_frame[0].content_document
        click_checkbox = await iframe_doc.find_element(By.XPATH, '//*[@id="challenge-stage"]/div/label/input', timeout=10)
        await click_checkbox.click()
    except Exception as e:
        print(f'ERROR CHECKBOX')

    try:
        await asyncio.sleep(5)
        await click(driver, 80, '//*[@id="header_fix"]/div/div[4]/div/a')
        await click(driver, 30, '//*[@id="deposit"]/div/div[4]/div[1]')
    except Exception as e:
        print(f'ERROR CHOOSE COINPAYMENTS \n{e}')

    try:
        await asyncio.sleep(2.5)
        await click(driver, 30, '//*[@id="CoinPayment_Banks"]')
        await asyncio.sleep(2.5)
        await driver.execute_script("document.getElementById('CoinPayment_Banks').value = 'USDT.TRC20';")
    except Exception as e:
        print(f"ERROR CHOOSE TRC20 \n{e}")

    try:
        await asyncio.sleep(2.4)
        find_frame = await driver.find_elements(By.TAG_NAME, 'iframe')
        await asyncio.sleep(0.6)
        iframe_doc = await find_frame[0].content_document
        click_checkbox = await iframe_doc.find_element(By.XPATH, '//*[@id="challenge-stage"]/div/label/input', timeout=10)
        await click_checkbox.click()
    except Exception as e:
        print(f'ERROR CHECKBOX')


    try:
        await asyncio.sleep(1)
        await input_data(driver, 30, '//*[@id="CoinPayment_Email"]', user_email)
        await input_data(driver, 30, '//*[@id="CoinPayment_Amount"]', '30')
    except Exception as e:
        print(f'ERROR INPUT MIN AMOUNT \n{e}')

    try:
        await click(driver, 30, '//*[@id="coinpayment"]/div[6]/a')
    except Exception as e:
        print(f'ERROR CLICK DEPOS BUT \n{e}')

    handles = await driver.window_handles
    print(handles)
    for handle in handles:
        await driver.switch_to.window(handle)
        title = await driver.title
        if not("et" in title):
            break


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(6.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="email-form"]/div[2]/div[1]/div[3]/div[2]', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="email-form"]/div[2]/div[1]/div[1]/div[2]', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT.TRC20", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
