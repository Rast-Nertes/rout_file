import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://spinsbro.com/en/login'
user_email = "kiracase34@gmail.com"
user_password = "5AZaaHTd8!LeGb"

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

    await driver.get(url)

    try:
        input_email = await driver.find_element(By.XPATH, '//*[@id="login"]', timeout=40)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.XPATH, '//*[@id="password"]', timeout=20)
        await input_pass.write(user_password)
    except Exception as e:
        return {"status":"0", "ext":f"error login data input {e}"}

    try:
        log_but = await driver.find_element(By.XPATH, '//*[@id="popupSubmit"]', timeout=40)
        await asyncio.sleep(1)
        await log_but.click()
    except Exception as e:
        return {"status":"0", "ext":f"error login {e}"}

    await asyncio.sleep(2.5)
    await driver.get('https://spinsbro.com/en/wallet/deposit', timeout=60)

    try:
        choose_bit = await driver.find_element(By.XPATH, '//img[@alt="Bitpace"]', timeout=20)
        await asyncio.sleep(1)
        await choose_bit.click()
    except Exception as e:
        return {"status":"0", "ext":f"error choose bitpace {e}"}

    try:
        depos = await driver.find_element(By.XPATH, '//*[@id="walletDepositSubmit"]', timeout=40)
        await asyncio.sleep(1)
        await depos.click()
    except Exception as e:
        return {"status":"0", "ext":f"error depos {e}"}

    await asyncio.sleep(5)
    wind = await driver.window_handles
    await driver.switch_to.window(wind[0])
    await asyncio.sleep(1.5)
    await driver.clear_proxy()
    await asyncio.sleep(1.5)
    await driver.set_single_proxy('http://WyS1nY:8suHN9@196.19.121.187:8000')
    await asyncio.sleep(1.5)
    await driver.refresh()
    await asyncio.sleep(1.5)

    try:
        choose_tether = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/ul/li[6]/div[1]/div/span', timeout=80)
        await asyncio.sleep(2.5)
        await driver.execute_script("arguments[0].click();", choose_tether)

        choose_trc20 = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/ul/li[6]/div[2]/ul/li[1]/a', timeout=60)
        await asyncio.sleep(1.5)
        await driver.execute_script("arguments[0].click();", choose_trc20)
    except Exception as e:
        return {"status":"0", "ext":f"error choose trc20 {e}"}

    try:
        pay_but = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/span[2]/button', timeout=80)
        await asyncio.sleep(2.5)
        await pay_but.click()
    except Exception as e:
        return {"status":"0", "ext":f"error pay button {e}"}


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(2.5)
        try:
            copy_amount = await driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/div/ul/li[1]/div/div[3]/a/span', timeout=60)
            await asyncio.sleep(2)
            await copy_amount.click()
            await asyncio.sleep(3.5)
            amount = pyperclip.paste()

            await asyncio.sleep(6.5)

            copy_address = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/ul/li[2]/div/div[3]/a/span', timeout=30)
            await asyncio.sleep(2)
            await copy_address.click()
            await asyncio.sleep(3.5)
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
