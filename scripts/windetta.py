import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://windetta.com/en'
user_email = "kiracase34@gmail.com"
user_password = "4ZzqWp2DmkvsC-B"


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
    await driver.get(url, timeout=90)

    try:
        await click(driver, 70, '//*[@id="headerSignInButton"]')
        await input_data(driver, 30, '//*[@id="login"]', user_email)
        await input_data(driver, 30, '//*[@id="password"]', user_password)
        await click(driver, 30, '//*[@id="popupSubmit"]')
    except Exception as e:
        print(f"ERROR LOGIN \n{e}")

    try:
        await click(driver, 30, '//*[@id="headerDepositButton"]')
        await click(driver, 30, '//img[@alt="Bitpace"]')
        await click(driver, 30, '//*[@id="cashierDepositSubmit"]')
    except Exception as e:
        print(f'ERROR CHOOSE BITPACE')

    await asyncio.sleep(4)
    wind = await driver.window_handles
    await driver.switch_to.window(wind[0])

    await driver.clear_proxy()
    await asyncio.sleep(5)
    await driver.set_single_proxy(f"http://WyS1nY:8suHN9@196.19.121.187:8000")
    await asyncio.sleep(1.5)
    await driver.refresh()
    await asyncio.sleep(1)

    try:
        choose_tether = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/ul/li[6]/div[1]/div/span', timeout=60)
        await asyncio.sleep(1)
        await driver.execute_script("arguments[0].click();", choose_tether)

        choose_trc20 = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/ul/li[6]/div[2]/ul/li[1]/a', timeout=40)
        await asyncio.sleep(1)
        await driver.execute_script("arguments[0].click();", choose_trc20)
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    try:
        pay_but = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/span[2]/button', timeout=20)
        await asyncio.sleep(1)
        await driver.execute_script("arguments[0].click();", pay_but)
    except Exception as e:
        print(f'ERROR PAY BUT \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            copy_amount = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/ul/li[1]/div/div[3]/a/span', timeout=20)
            await asyncio.sleep(2.5)
            await copy_amount.click()

            await asyncio.sleep(1.5)
            amount = pyperclip.paste()

            await asyncio.sleep(1)
            await driver.execute_script("window.scrollBy(0, 200);")
            await asyncio.sleep(4.5)

            copy_address = await driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/div/ul/li[2]/div/div[3]/a', timeout=20)
            await asyncio.sleep(2.5)
            await copy_address.click()

            await asyncio.sleep(1.5)
            address = pyperclip.paste()

            return {
                "address": address,
                "amount": amount.replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)