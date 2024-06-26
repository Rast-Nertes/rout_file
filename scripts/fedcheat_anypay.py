import asyncio

from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

url = 'https://fedcheat.ru/game/AmazingOnline.html'
user_email = 'rwork875@gmail.com'
user_name = "rwork875"
user_password = "092841e92L12"

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

#092841e92L12

async def login(driver):
    await driver.get('https://fedcheat.ru/auth')
    await driver.maximize_window()

    try:
        input_email = await driver.find_element(By.ID, 'name', timeout=20)
        await input_email.write(user_name)
        await asyncio.sleep(1)
        input_pass = await driver.find_element(By.ID, 'password', timeout=20)
        await input_pass.write(user_password)
        await asyncio.sleep(1)
        click_log_but = await driver.find_element(By.ID, 'authButton', timeout=20)
        await asyncio.sleep(1.5)
        await click_log_but.click()
    except Exception as e:
        print(f'ERROR LOG \n{e}')

    await asyncio.sleep(3.5)
    await driver.get(url)

    try:
        choose_tov = await driver.find_element(By.XPATH, '/html/body/div[2]/main/section[1]/div/div/div[2]/a[2]/div/div[1]',timeout=35)
        await asyncio.sleep(1.5)
        await choose_tov.click()
    except Exception as e:
        print(f"ERROR CHOOSE TOV \n{e}")

    try:
        buy_but = await driver.find_element(By.XPATH, '/html/body/div[2]/main/section[2]/div/div/div/div[3]/button', timeout=20)
        await asyncio.sleep(1.5)
        await buy_but.click()
    except Exception as e:
        print(f'ERROR BUY BUT \n{e}')

    try:
        choose_usdt = await driver.find_element(By.CSS_SELECTOR, 'div.list > div.usdt', timeout=20)
        await asyncio.sleep(1.5)
        await choose_usdt.click()
    except Exception as e:
        print(f'ERROR CHOOSE USDT \n{e}')

    try:
        input_em = await driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/form/div[3]/fieldset/input', timeout=20)
        await input_em.write(user_email)
        await asyncio.sleep(0.5)

        next_step_but = await driver.find_element(By.XPATH, '/html/body/main/div[2]/div[2]/form/div[4]/button', timeout=20)
        await asyncio.sleep(1)
        await next_step_but.click()
    except Exception as e:
        print(f"ERROR NEXT STEP \n{e}")


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(2.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '/html/body/main/div[2]/div/form/div[2]/fieldset/input', timeout=30)
            address = await address_elem.__getattribute__('value')

            amount_elem = await driver.find_element(By.XPATH, '/html/body/main/div[2]/div/form/div[1]/div[2]/span', timeout=30)
            amount = await amount_elem.text

        except Exception as e:
            print(f"ERROR DATA \n{e}")

        return {
            "address": address,
            "amount": amount.replace("USDT", '').replace(" ", ''),
            "currency": "usdt"
        }


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
