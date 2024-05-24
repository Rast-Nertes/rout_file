import asyncio
import pyautogui
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://brillx51.gg/'
user_email = "kiracase34"
user_password = "kiramira123"

# CHROME CONSTANTS

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
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    try:
        await click(driver, 50, '//*[@id="header"]/div/div[2]/div/button[1]')
        await input_data(driver, 40, '//*[@id="inputLogin"]', user_email)
        await input_data(driver, 30, '//*[@id="inputPassword"]', user_password)
        await click(driver, 30, '/html/body/div[5]/div/div[1]/div/div/div/div[2]/div/div[4]/button')
    except Exception as e:
        return {"status":"0", "ext":f"error login: {e}"}

    try:
        await asyncio.sleep(2.5)
        await click(driver, 30, '//*[@id="header"]/div/div[2]/div/div[1]/div/button')
        await click(driver, 30, "//button[@type='button' and @value='withdraw' and contains(text(), 'Cryptocurrency')]")
    except Exception as e:
        return {"status":"0", "ext":f"error cryptocurrency  {e}"}

    try:
        await click(driver, 30, "//button[@type='button' and .//span[text()='TRC20']]")
    except Exception as e:
        return {"status":"0", "ext":f"error choose trc20:  {e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//input[@name="address"]', timeout=30)
            address = await address_elem.get_attribute('value')

            amount_elem = await driver.find_element(By.XPATH, '/html/body/div[6]/div/div[1]/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/span', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("Tether", '').replace("\xa0", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
