from time import sleep
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent
import asyncio

#CONSTANS

url = "http://safeassets.com"
user_login = 'alex37347818'
user_password = 'a5NvMaGjExXU@@a'

#CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.binary_location = chrome_path

#PROXY CONSTANS
proxy_name = 'WyS1nY'
proxy_pass = '8suHN9'
proxy_port = '8000'
proxy_ip = "196.19.121.187"


async def login(driver):
    await driver.set_single_proxy(f"http://{proxy_name}:{proxy_pass}@{proxy_ip}:{proxy_port}")
    sleep(1)
    await driver.get('https://www.safeassets.com/login/say/invalid_login/e/username')
    await driver.maximize_window()
    
    try:
        find_frame = await driver.find_element(By.TAG_NAME, 'iframe', timeout=15)
        await asyncio.sleep(1)
        iframe_document = await find_frame[0].content_document

        checkbox = await iframe_document.find_element(By.CSS_SELECTOR, 'challenge-stage > div > label > input[type=checkbox] - checkbox', timeout=20)
        await asyncio.sleep(10)
        await driver.execute_script("arguments[0].click();", checkbox)
    except Exception as e:
        print(f"CLICK \n{e}")

    try:
        input_email = await driver.find_element(By.ID, 'el-2', timeout=15)
        sleep(1.5)
        await input_email.clear()
        await input_email.write(user_login)

        input_password = await driver.find_element(By.ID, 'el-3', timeout=15)
        sleep(1.5)
        await input_password.clear()
        await input_password.write(user_password)
    except Exception as e:
        print(f"INPUT DATA ERROR \n{e}")

    try:
        login_button = await driver.find_element(By.CSS_SELECTOR,
                                                 'body > div.wrapper > main > div > div.popup > form > div:nth-child(8) > button',
                                                 timeout=10)
        await driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"ERROR BUTTON LOGIN \n{e}")


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        sleep(3)
        await driver.get('https://www.safeassets.com/deposit')


        try:
            choose_trc20 = await driver.find_element(By.CSS_SELECTOR, 'div.page__el.page__el_acc > div.payments-grid.payments__options.payments-custom > div > div:nth-child(11) > div > div > div.options > div:nth-child(1) > label', timeout=50)
            await driver.execute_script("arguments[0].click();", choose_trc20)

            choose_trc20_step2 = await driver.find_element(By.CSS_SELECTOR, 'div.page__el.page__el_acc > div:nth-child(4) > div > div.plans__items > div:nth-child(1) > label', timeout=20)
            await driver.execute_script("arguments[0].click();", choose_trc20_step2)
        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")

        try:
            make_depos = await driver.find_element(By.CSS_SELECTOR, 'div.page__el.page__el_acc > div:nth-child(4) > div > div.range-calk.page__el > div.range-calk__rigth.shadow2 > button', timeout=10)
            await driver.execute_script("arguments[0].click();", make_depos)
        except Exception as e:
            print(f"MAKE DEPOS ERROR \n{e}")
        
        try:
            amount_element = await driver.find_element(By.CSS_SELECTOR, 'body > div.wrapper > main > div > table > tbody > tr:nth-child(8) > td', timeout=10)
            amount = await amount_element.text

            address_element = await driver.find_element(By.CSS_SELECTOR, '#usdt\.trc20_form > i > a', timeout=10)
            address = await address_element.text

            return {
                "address": address.replace("(Token USDT)", "").replace(" ", ''),
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
