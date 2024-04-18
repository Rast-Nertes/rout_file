import asyncio
import pyautogui
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://icloudminer.com/user/login'
user_email = "lasawo9725@rartg.com"
user_password = "Qwerty62982."

# CHROME CONSTANTS

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()

options.binary_location = chrome_path


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    try:
        input_name = await driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/form/div[2]/input', timeout=30)
        await input_name.write(user_email)

        input_pass = await driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div/form/div[3]/input', timeout=20)
        await input_pass.write(user_password)
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    try:
        click_log = await driver.find_element(By.XPATH, '//*[@id="recaptcha"]', timeout=20)
        await asyncio.sleep(4)
        await click_log.click()
    except Exception as e:
        print(f'ERROR CLICK LOG \n{e}')

    await asyncio.sleep(2.5)
    await driver.get('https://icloudminer.com/user/deposit-money')

    try:
        select = await driver.find_element(By.XPATH, '/html/body/section/div/div/div/form/div/div[1]/div[1]/select', timeout=30)
        await asyncio.sleep(1.5)
        await select.click()

        for _ in range(5):
            pyautogui.press('down')
            await asyncio.sleep(0.5)
        pyautogui.press("enter")

        input_amount = await driver.find_element(By.XPATH, '/html/body/section/div/div/div/form/div/div[1]/div[2]/div/input', timeout=20)
        await asyncio.sleep(1.5)
        await input_amount.write('100')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    try:
        click_log = await driver.find_element(By.XPATH, '/html/body/section/div/div/div/form/div/div[2]/button', timeout=20)
        await asyncio.sleep(1)
        await click_log.click()
    except Exception as e:
        print(f'ERROR CLICK LOG \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="coin_wallet_address"]', timeout=30)
            address = await address_elem.__getattribute__('value')

            amount_elem = await driver.find_element(By.XPATH, '/html/body/section/div/div/div/div/div/div/div[1]/p[1]/b[2]/font/font', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("долларов США", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
