import asyncio
import re
import pyautogui
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://smspva.com/signin.html'
user_login = 'kiracase34@gmail.com'
user_password = 'kirapva122'

# CHROME CONSTANTS


options = webdriver.ChromeOptions()
options.add_argument("--disable-save-password-bubble")
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
    await driver.get(url, timeout=60)

    try:
        await input_data(driver, 30, '//*[@id="login"]', user_login)
        await input_data(driver, 30, '//*[@id="password"]', user_password)
        await asyncio.sleep(3)
        await click(driver, 30, '(//button[@name="submit"])[1]')
    except Exception as e:
        return {"status": "0", "ext": f"Login error \n{e}"}

    await asyncio.sleep(3)
    await driver.get('https://smspva.com/pay-systems.html/crypto_coins')

    try:
        await click(driver, 10, '(//button[@type="button"])[1]')
    except:pass

    try:
        await input_data(driver, 10, '//input[@name="amountUSD"]', '3')
    except Exception as e:
        print(f'ERROR INPUT AMOUNT \n{e}')

    try:
        await asyncio.sleep(1.5)
        await click(driver, 30, '//*[@id="payment_systems"]/div[2]/div/form/div/div[2]/div/label[3]/div')
        await click(driver, 10, '//button[@title]')
    except Exception as e:
        return {"status": "0", "ext": f"DEPOS BUT \n{e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="__next"]/main/section/div/div[1]/div[1]/div[1]/div[3]/div[2]/p', timeout=20)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="__next"]/main/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/p', timeout=20)
            amount = await amount_elem.text

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
