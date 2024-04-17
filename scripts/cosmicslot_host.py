import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://cosmicslot.com/en/?cashier=is_open'
user_email = "kiracase34@gmail.com"
user_password = "HRAuiCAX8u@hcw"

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


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    try:
        input_email = await driver.find_element(By.XPATH, '//*[@id="loginModal___BV_modal_body_"]/div/div[1]/form/div/label[1]/input', timeout=30)
        await input_email.write(user_email)

        input_password = await driver.find_element(By.XPATH, '//*[@id="loginModal___BV_modal_body_"]/div/div[1]/form/div/label[2]/input', timeout=20)
        await input_password.write(user_password)
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    try:
        click_log = await driver.find_element(By.XPATH, '//*[@id="loginModal___BV_modal_body_"]/div/div[1]/form/button[2]', timeout=20)
        await asyncio.sleep(1)
        await click_log.click()
    except Exception as e:
        print(f'ERROR CLICK LOG \n{e}')

    await asyncio.sleep(2.5)
    await driver.get('https://cosmicslot.com/en/account/myRoom')

    try:
        click_depos_but = await driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div/div[1]/div[4]/div[3]/button', timeout=20)
        await asyncio.sleep(1.5)
        await driver.execute_script("arguments[0].click();", click_depos_but)
    except Exception as e:
        print(f'ERROR CLICK DEPOS BUT \n{e}')

    try:
        choose_trc20 = await driver.find_element(By.XPATH, '//*[@id="WalletModal___BV_modal_body_"]/div[2]/div[2]/div[1]/div[4]/div/button[13]', timeout=20)
        await asyncio.sleep(1)
        await choose_trc20.click()

        depos_but = await driver.find_element(By.XPATH, '//*[@id="WalletModal___BV_modal_body_"]/div[2]/div[2]/div[2]/div/form/div/div[2]/div[3]/button', timeout=20)
        await asyncio.sleep(1)
        await depos_but.click()
    except Exception as e:
        print(f'ERROR DEPOS BUT \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(1.5)
        try:
            copy_address = await driver.find_element(By.XPATH, '//*[@id="cryptoPopup___BV_modal_body_"]/div/div[2]/button', timeout=20)
            await asyncio.sleep(1)
            await copy_address.click()

            await asyncio.sleep(1.5)
            address = pyperclip.paste()

            await asyncio.sleep(3.5)

            copy_amount = await driver.find_element(By.XPATH, '//*[@id="cryptoPopup___BV_modal_body_"]/div/p', timeout=20)
            amount = await copy_amount.text

            return {
                "address": address,
                "amount": amount.replace("USDTT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
