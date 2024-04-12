import asyncio
from flask import jsonify
from anticaptchaofficial.recaptchav2proxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

url = 'https://fairspin.io'
user_email = "rwork875@gmail.com"
user_password = "111jdy123h1L"
site_key = '6LfW3hgoAAAAAHj6u5ZT8A10DhcTJ9bqQaheVZII'

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[2].strip()

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.binary_location = chrome_path
# options.add_extension(ext)
#111jdy123h1L


def captcha_solver():
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(api_key)
    solver.set_website_url(url)
    solver.set_website_key(site_key)

    g_response = solver.solve_and_return_solution()
    return g_response


async def login(driver):
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await driver.get(url, timeout=60)
    await driver.maximize_window()

    try:
        await asyncio.sleep(1.5)
        log_but = await driver.find_element(By.XPATH, '//*[@id="app-header"]/div/div[2]/div/a[1]/button', timeout=20)
        await asyncio.sleep(1)
        await log_but.click()

        await asyncio.sleep(5.5)
        result_captcha = captcha_solver()
        input_captcha_code = await driver.find_element(By.TAG_NAME, 'textarea')
        await driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)

        input_email = await driver.find_element(By.XPATH, "//input[@name='email']", timeout=20)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.XPATH, "//input[@name='password']", timeout=20)
        await input_pass.write(user_password)

        log_but_click = await driver.find_element(By.CSS_SELECTOR, 'div.base-dialog__body > div.auth-view-common-promo-dialog__body > form > div.auth-sign-in__actions > button > span.q-btn__content.text-center.col.items-center.q-anchor--skip.justify-center.row', timeout=20)
        await asyncio.sleep(1)
        await log_but_click.click()
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        await asyncio.sleep(2)
        await driver.get('https://fairspin.io/ru/cashier/deposit')
    except Exception as e:
        print(f'ERROR A HREF \n{e}')

    try:
        choose_usdt = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div/div[2]/div/div/div/div/div[2]/div[2]/div[2]/div/a[1]', timeout=20)
        await asyncio.sleep(1)
        await choose_usdt.click()

        input_amount = await driver.find_element(By.XPATH, '//*[@id="amount"]', timeout=20)
        await asyncio.sleep(1)
        await input_amount.clear()
        await input_amount.write('5')

        take_usdt = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div/div[2]/div/div/div[2]/div[1]/div[1]/button/span[2]', timeout=20)
        await asyncio.sleep(1)
        await take_usdt.click()

        choose_trc20 = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div/div[2]/div/div/div[2]/div/div/div[3]/div[1]', timeout=20)
        await asyncio.sleep(1)
        await choose_trc20.click()

        accept = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div/div[2]/div/div/div[2]/div/div/button/span[2]', timeout=20)
        await asyncio.sleep(1)
        await accept.click()
    except Exception as e:
        print(f'ERROR TAKE USDT ERROR \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.CSS_SELECTOR, 'div.cashier-deposit-field > div.cashier-deposit-field__input > div.cashier-deposit-field__value', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.CSS_SELECTOR, 'div.base-block.base-block--offset.base-block--primary.cashier-deposit-crypto__block > div.cashier-deposit-crypto-hint > span', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
