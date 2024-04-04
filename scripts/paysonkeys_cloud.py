import asyncio

from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

url = 'https://paysonkeys.com/pubg-mobile/android/shield-pubgm'
user_email = "yewoxo4550@otemdi.com"
user_password = "Qwerty62982"

# CHROME CONSTANS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.binary_location = chrome_path


async def login(driver):
    await driver.get(url)
    await driver.maximize_window()

    try:
        click_log = await driver.find_element(By.ID, 'block-user', timeout=20)
        await driver.execute_script("arguments[0].click();", click_log)
    except Exception as e:
        print(f"ERROR CHOOSE \n{e}")

    try:
        input_username = await driver.find_element(By.ID, 'username', timeout=20)
        await input_username.write(user_email)

        sleep(1.5)

        input_username = await driver.find_element(By.ID, 'password', timeout=20)
        await input_username.write(user_password)

        await asyncio.sleep(7.5)

        log_button = await driver.find_element(By.XPATH, '//*[@id="auth"]/div/div/button[1]', timeout=20)
        await log_button.click()
    except Exception as e:
        print(f"INPUT LOG ERROR \n{e}")
    #
    # await asyncio.sleep(2.5)
    # await driver.get('https://paysonkeys.com/my/profile')
    #
    # input("press")
    try:
        await asyncio.sleep(1.5)
        buy_but = await driver.find_element(By.XPATH, '/html/body/div[2]/main/section[1]/div/div[1]/div[2]/div[2]/button', timeout=20)
        await buy_but.click()
        await asyncio.sleep(1.5)
        next_step_but = await driver.find_element(By.XPATH, '//*[@id="body"]/div[1]/button', timeout=20)
        await driver.execute_script("arguments[0].click();", next_step_but)
    except Exception as e:
        print(f"ERROR CHECKBOX \n{e}")

    try:
        await asyncio.sleep(1.5)
        choose_crypto = await driver.find_element(By.XPATH, '//*[@id="buy-payments-methods"]/label[7]', timeout=20)
        await driver.execute_script("arguments[0].click();", choose_crypto)
        await asyncio.sleep(3.5)
        buy_but_next_step = await driver.find_element(By.XPATH, '//*[@id="btn-pay"]', timeout=20)
        await driver.execute_script("arguments[0].click();", buy_but_next_step)
    except Exception as e:
        print(f"ERROR CHOOSE CRYPTO \n{e}")

    try:
        await asyncio.sleep(2.5)
        handles = await driver.window_handles

        for handle in handles:
            await asyncio.sleep(1.5)
            await driver.switch_to.window(handle)
            title = await driver.title
            if ("Оплата" in title) or ("Подождите" in title):
                break
    except Exception as e:
        print(f"ERROR CHOOSE \n{e}")

    try:
        input_email_in_payment = await driver.find_element(By.ID, 'details_email', timeout=20)
        await input_email_in_payment.write(user_email)
        await asyncio.sleep(1)
        next_but = await driver.find_element(By.XPATH, '//*[@id="payment_proceed_details"]/div[2]/button', timeout=20)
        await driver.execute_script("arguments[0].click();", next_but)
    except Exception as e:
        print(f"ERROR NEXT BUT \n{e}")

    try:
        await asyncio.sleep(1.5)
        choose_trc20 = await driver.find_element(By.XPATH, '//*[@id="payment_form"]/div[13]', timeout=20)
        await driver.execute_script("arguments[0].click();", choose_trc20)
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        sleep(4.5)
        try:
            address_elem = await driver.find_element(By.ID, 'crypto_address', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.ID, 'pay_amount', timeout=30)
            amount = await amount_elem.text

        except Exception as e:
            print(f"ERROR DATA \n{e}")

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)