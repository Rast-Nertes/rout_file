import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://icebet.casino/en/wallet/deposit'
user_email = "kiracase34@gmail.com"
user_password = "Q!fgUmpD7cTCV"

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
        input_email = await driver.find_element(By.XPATH, '//*[@id="login"]', timeout=30)
        await input_email.write(user_email)

        input_password = await driver.find_element(By.XPATH, '//*[@id="password"]', timeout=20)
        await input_password.write(user_password)
    except Exception as e:
        print(f'ERROR LOG DATA \n{e}')

    try:
        click_log_but = await driver.find_element(By.XPATH, '//*[@id="popupSubmit"]', timeout=30)
        await asyncio.sleep(1.5)
        await click_log_but.click()
    except Exception as e:
        print(f"ERROR CLICK LOG BUT \n{e}")

    try:
        click_bit = await driver.find_element(By.XPATH, '//img[@alt="Bitpace"]', timeout=20)
        await asyncio.sleep(1.5)
        await click_bit.click()
    except Exception as e:
        input_elem = await driver.find_element(By.XPATH, '//*[@id="login-field"]', timeout=30)
        if input_elem:
            return {"status": "0", "ext":"Login error. Check script."}

    try:
        click_depos = await driver.find_element(By.XPATH, '//*[@id="walletDepositSubmit"]', timeout=20)
        await asyncio.sleep(1.5)
        await click_depos.click()
    except Exception as e:
        print(f'ERROR CLICK DEPOS \n{e}')

    await asyncio.sleep(5.5)
    wind = await driver.window_handles

    for window in wind:
        await driver.switch_to.window(window)
        title = await driver.title
        print(title)
        if not("Ice" in title):
            break

    await driver.clear_proxy()
    await asyncio.sleep(2.5)
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

        await asyncio.sleep(1.5)
        try:
            copy_address = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/ul/li[2]/div/div[3]/a', timeout=20)
            await asyncio.sleep(1)
            await copy_address.click()

            await asyncio.sleep(2.5)
            address = pyperclip.paste()

            await asyncio.sleep(3.5)

            copy_amount = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/ul/li[1]/div/div[3]/a', timeout=20)
            await asyncio.sleep(2.5)
            await copy_amount.click()

            await asyncio.sleep(1.5)
            amount = pyperclip.paste()

            return {
                "address": address,
                "amount": amount.replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
