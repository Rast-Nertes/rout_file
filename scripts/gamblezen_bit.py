import asyncio
import pyperclip
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://gamblezen.com/'
user_email = "kiracase34@gmail.com"
user_password = ".VXs43T3S4LhyRq"

# CHROME CONSTANTS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

# COOKIES
# options.binary_location = chrome_path
# options.add_extension(ext)


async def login(driver):
    await driver.maximize_window()

    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await driver.get(url, timeout=60)

    try:
        log_but = await driver.find_element(By.XPATH, '//*[@id="headerSignInButton"]', timeout=45)
        await asyncio.sleep(1)
        await log_but.click()
    except Exception as e:
        print(f'ERROR LOG BUTTON \n{e}')

    try:
        input_email = await driver.find_element(By.XPATH, '//*[@id="login"]', timeout=20)
        await input_email.write(user_email)

        input_password = await driver.find_element(By.XPATH, '//*[@id="password"]', timeout=20)
        await input_password.write(user_password)

        login_button = await driver.find_element(By.XPATH, '//*[@id="popupSubmit"]', timeout=20)
        await asyncio.sleep(1)
        await login_button.click()
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        dpos_but = await driver.find_element(By.XPATH, '//*[@id="headerDepositButton"]', timeout=30)
        await asyncio.sleep(1)
        await dpos_but.click()
    except Exception as e:
        print(f'ERROR DEPOS BUTTON \n{e}')

    try:
        choose_bit = await driver.find_element(By.XPATH, '//*[@id="walletDepositPaymentList"]/div[3]/div/div[9]', timeout=30)
        await asyncio.sleep(1)
        await choose_bit.click()
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    try:
        click_depos_but = await driver.find_element(By.XPATH, '//*[@id="cashierDepositSubmit"]', timeout=20)
        await asyncio.sleep(1)
        await click_depos_but.click()
    except Exception as e:
        print(f'ERROR DEPOS BUT \n{e}')

    await asyncio.sleep(2)
    wind = await driver.window_handles
    await driver.switch_to.window(wind[0])

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
        await login(driver)

        await asyncio.sleep(1.5)
        try:
            copy_address = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/ul/li[2]/div/div[3]/a', timeout=20)
            await asyncio.sleep(1)
            await copy_address.click()

            await asyncio.sleep(1.5)
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

