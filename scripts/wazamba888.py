import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'http://wazamba-1002.com'
user_email = "rwork875"
user_password = "hqwl3WEl12"

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
    await asyncio.sleep(1)
    await find_input.write(data)


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=120)

    try:
        await asyncio.sleep(1.5)
        await click(driver, 20, '/html/body/ui-view/ui-view/linda-app/ui-view/linda-view-layer-one/linda-sidebar/div/div[2]/div[2]/a[1]')
    except Exception as e:
        print(f'ERROR CLICK LOG \n{e}')

    try:
        await input_data(driver, 20, '/html/body/linda-popup-body/div/linda-login-popup/linda-login-form/div/div/div[2]/form/div[1]/input', user_email)
        await input_data(driver, 20, '/html/body/linda-popup-body/div/linda-login-popup/linda-login-form/div/div/div[2]/form/div[3]/input', user_password)
        await asyncio.sleep(1.5)
        await click(driver, 20, '/html/body/linda-popup-body/div/linda-login-popup/linda-login-form/div/div/div[2]/form/div[4]/button')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        await click(driver, 20, '/html/body/ui-view/ui-view/linda-app/ui-view/linda-view-layer-one/ui-view/linda-view-layer-three/div/div[3]/batman-ui-wrapper3/div[1]/div[3]/div[1]/button')
    except Exception as e:
        find_input_tag = await driver.find_element(By.XPATH,
                                                   '/html/body/linda-popup-body/div/linda-login-popup/linda-login-form/div/div/div[2]/form/div[1]/input',
                                                   timeout=10)
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"ERROR DEPOS BUT \n{e}")

    try:
        await click(driver, 20, '/html/body/linda-popup-body/div/linda-cashbox-popup/div/div[4]/div[2]/batman-cashbox-deposit1/div[2]/div[1]/div[2]/div[11]')
    except Exception as e:
        print(f'ERROR CLICK DEPOS \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        amount_elem = await driver.find_element(By.XPATH, '/html/body/linda-popup-body/div/linda-cashbox-popup/div/div[4]/div[2]/linda-cashbox-deposit-form/form/div[3]/div[2]/div[1]', timeout=20)
        amount = await amount_elem.text

        try:
            await click(driver, 30, '/html/body/linda-popup-body/div/linda-cashbox-popup/div/div[4]/div[2]/linda-cashbox-deposit-form/form/div[3]/div[2]/div[1]')
        except Exception as e:
            print(f'ERROR CHOOSE AMOUNT \n{e}')

        try:
            await click(driver, 20,
                        '/html/body/linda-popup-body/div/linda-cashbox-popup/div/div[4]/div[2]/linda-cashbox-deposit-form/form/div[4]/div[2]/button')
        except Exception as e:
            print(f'ERROR DEPOS \n{e}')

        await asyncio.sleep(4)
        winds = await driver.window_handles
        for window in winds:
            await asyncio.sleep(1)
            await driver.switch_to.window(window)
            title = await driver.title
            print(title)
            if "gat" in title:
                break

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.CLASS_NAME, 'wallet-address', timeout=30)
            address = await address_elem.text

            return {
                "address": address,
                "amount": amount.replace(" ", '').replace("€", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
