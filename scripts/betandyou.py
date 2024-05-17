import asyncio
import pyautogui
from anticaptchaofficial.imagecaptcha import *
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://betandyou.com/en'
user_email = "869260631"
user_password = "wbUvNDDbLVSsD2e"


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
    ext = paths[1].strip()

options.binary_location = chrome_path


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
        await click(driver, 12, '//*[@id="modals-container"]/div/div/div[2]/div/button')
        await asyncio.sleep(3.5)
        await click(driver, 6, '//*[@id="modals-container"]/div/div/div[2]/div/button')
    except:
        pass

    await asyncio.sleep(1.5)

    try:
        await click(driver, 30, '//*[@id="app"]/div[3]/header/div[2]/span[3]/div/div/button')
    except Exception as e:
        return {"status":'0', "ext":f"error log button \n{e}"}

    try:
        await asyncio.sleep(2.5)
        await input_data(driver, 30, '/html/body/div[1]/div/div/div[3]/header/div[2]/span[3]/div/div[2]/div/div/div/form/div[2]/div/input', user_email)
        await input_data(driver, 30, '/html/body/div[1]/div/div/div[3]/header/div[2]/span[3]/div/div[2]/div/div/div/form/div[3]/div/input', user_password)
    except Exception as e:
        return {"status": '0', "ext": f"error input log data \n{e}"}

    await asyncio.sleep(1.5)

    try:
        await click(driver, 30, '//*[@id="app"]/div[3]/header/div[2]/span[3]/div/div[2]/div/div/div/form/button')
    except Exception as e:
        return {"status": '0', "ext": f"error login finish button \n{e}"}

    await asyncio.sleep(5)
    await driver.get('https://betandyou.com/en/office/recharge')

    await asyncio.sleep(3)
    find_frame = await driver.find_elements(By.XPATH, '//*[@id="payments_frame"]')
    await asyncio.sleep(0.5)
    frame = await find_frame[0].content_document

    try:
        click_trc20 = await frame.find_element(By.XPATH, '//div[@data-method="usdttrx"]', timeout=20)
        await asyncio.sleep(1.5)
        await click_trc20.click()

        click_confirm = await frame.find_element(By.XPATH, '//*[@id="payment_modal_container"]/div[2]/form/div[3]/div/div[1]/button', timeout=20)
        await asyncio.sleep(1.5)
        await click_confirm.click()
    except Exception as e:
        print(f'ERROR FRAME \n')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(3)
        find_frame = await driver.find_elements(By.XPATH, '//*[@id="payments_frame"]')
        await asyncio.sleep(0.5)
        frame = await find_frame[0].content_document

        await asyncio.sleep(4.5)
        try:
            address_elem = await frame.find_element(By.XPATH, '//*[@id="crypto_wallet"]', timeout=30)
            address = await address_elem.text

            amount_elem = await frame.find_element(By.XPATH, '//*[@id="payment_modal_container"]/div[2]/form/div[4]/div/div[1]/div[1]/span', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("Minimum deposit amount", "").replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
