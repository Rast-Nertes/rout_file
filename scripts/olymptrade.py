import asyncio
import pyperclip
from twocaptcha import TwoCaptcha
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://olymptrade.com/login'
user_email = "leonidstakanov11@gmail.com"
user_password = "Qwerty17"

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
    api_key = paths[3].strip()
    ext = paths[1].strip()

options.binary_location = chrome_path
# options.add_extension(ext)
#6Lc5ACgTAAAAABL3s8j9VkkUn4Engv4QtdCLd9qI


def captcha_solve():
    solver = TwoCaptcha(api_key)
    result = solver.recaptcha(sitekey='6Lc5ACgTAAAAABL3s8j9VkkUn4Engv4QtdCLd9qI',
                              url=url)

    return result['code']


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
    # await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    try:
        await click(driver, 30, '//button[@data-test="form-tab-signin"]')
        await input_data(driver, 30, '//input[@name="email"]', user_email)
        await input_data(driver, 30, '//input[@name="password"]', user_password)
        await click(driver, 30, '//div[@data-test="buttonContentBox"]')
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    await asyncio.sleep(2.5)

    try:
        input_captcha_code = await driver.find_element(By.TAG_NAME, 'textarea', timeout=6.5)
        result_captcha = captcha_solve()
        await driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)
        await asyncio.sleep(2.5)

        await click(driver, 30, '//div[@data-test="buttonContentBox"]')
    except:
        pass

    while True:
        try:
            text_catpcha = await driver.find_element(By.XPATH, '//*[@id="page-container"]/div[3]/div/div/div[2]/div/div[2]/div/form/div[4]/div/p', timeout=6.5)
            text = await text_catpcha.text
            if "робот" in text:
                result_captcha = captcha_solve()
                input_captcha_code = await driver.find_element(By.TAG_NAME, 'textarea', timeout=20)
                await driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)
                await asyncio.sleep(2.5)

                await click(driver, 30, '//div[@data-test="buttonContentBox"]')
            else:
                break
        except:
            break

    try:
        await click(driver, 30, '//p[@data-test="account-balance-value"]')
        await click(driver, 30, '//*[@id="page-container"]/div/div[7]/div[2]/div/div[2]/div/div/div/div[3]')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    try:
        await click(driver, 30, '//*[@id="page-container"]/div/div[7]/div[2]/div/div[2]/div/div/div/div[3]/div[2]/button[2]/div')
        await click(driver, 30, '//*[@id="page-container"]/div/div[7]/div[2]/div/div[2]/div/div/div[2]/div[2]/button/div')
        await click(driver, 30, '//*[@id="page-container"]/div/div[7]/div[2]/div/div[2]/div/div/div[2]/div[2]/button[8]')
        await click(driver, 30, '//*[@id="page-container"]/div/div[7]/div[2]/div/div[2]/div/div/div[2]/div[5]/button/div/div/div/div')
    except Exception as e:
        print(f'ERROR DEPOS MIN AMOUNT \n{e}')

    try:
        await click(driver, 30, '//*[@id="page-container"]/div/div[7]/div[2]/div/div[2]/div/div/div[3]/button/div/div/div/div')
    except Exception as e:
        print(f'ERROR CONFIRM BUT \n{e}')

    find_src = await driver.find_element(By.XPATH, '//*[@id="payment_form"]', timeout=30)
    scr = await find_src.get_attribute('action')
    await asyncio.sleep(1)
    await driver.get(scr)

    try:
        await click(driver, 30, '//*[@id="root"]/div/div/div[1]/div/div[1]/div[1]/div/button/div')
    except Exception as e:
        print(f'ERROR SHOW ME BUT \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            amount_elem = await driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div[3]/div[1]/div/div[1]/div/p', timeout=30)
            amount = await amount_elem.text

            address_elem = await driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div[1]/div/div[3]/div[1]/div/div/p', timeout=30)
            address = await address_elem.text

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
