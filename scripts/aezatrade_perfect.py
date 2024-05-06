import asyncio
import pyperclip
from anticaptchaofficial.imagecaptcha import *
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://aezatrade.pro/platform/auth/login'
user_email = "rwork875@gmail.com"
user_password = "83dla3k12ak2"
perfect_id = '84286029'
perfect_pass = 'kdUqfuz1'

# CHROME CONSTANTS

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[2].strip()
    ext = paths[4].strip()

options.binary_location = chrome_path
options.add_extension(ext)


def captcha_solver():
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(api_key)

    captcha_text = solver.solve_and_return_solution("captcha.png")
    time.sleep(1)

    if captcha_text != 0:
        print("captcha text " + captcha_text)
    else:
        print("task finished with error " + solver.error_code)

    return captcha_text


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
        await input_data(driver, 30, '//input[@placeholder="E-mail"]', user_email)
        await asyncio.sleep(6.5)
        await input_data(driver, 30, '//*[@id="app"]/form/div[3]/input', user_password)
        await asyncio.sleep(6.5)
        await click(driver, 30, '//*[@id="app"]/form/button[2]')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        await click(driver, 60, '//*[@id="app"]/header[1]/a[2]')
    except Exception as e:
        find_input_tag = await driver.find_element(By.XPATH, '//input[@placeholder="E-mail"]', timeout=7.5)
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"ERROR DEPOS BUT \n{e}")

    try:
        await click(driver, 30, '//*[@id="app"]/div[1]/div[3]/div/button[10]')
    except Exception as e:
        print(f'ERROR CLICK CRYPTO \n{e}')

    try:
        await input_data(driver, 30, '//*[@id="app"]/div[1]/div[2]/form/div[1]/input', '10')
        await click(driver, 30, '//*[@id="app"]/div[1]/div[2]/form/button')
    except:
        print(f'ERROR CHOOSE PERFECT MONEY \n{e}')

    try:
        await click(driver, 30, '//*[@id="r_crypto"]')
        await click(driver, 30, '//input[@name="action"]')
    except Exception as e:
        print(f'ERROR LOGIN PERFECT \n{e}')

    try:
        while True:
            try:
                find_captcha = await driver.find_element(By.XPATH, '//*[@id="f_log"]/table[1]/tbody/tr/td/table/tbody/tr[3]/td[2]/input', timeout=7.5)
            except Exception as e:
                print(f"ERROR \n{e}")
                break

            await asyncio.sleep(2.5)

            try:
                await input_data(driver, 30, '//input[@name="Login"]', perfect_id)
                await input_data(driver, 30, '//*[@id="keyboardInputInitiator0"]', perfect_pass)
            except Exception as e:
                print(f'ERROR CLICK \n{e}')

            image_captcha = await driver.find_element(By.XPATH, '//*[@id="cpt_img"]', timeout=20)
            await image_captcha.screenshot('captcha.png')

            result = captcha_solver()
            await asyncio.sleep(1.5)

            await input_data(driver, 30, '//*[@id="f_log"]/table[1]/tbody/tr/td/table/tbody/tr[3]/td[2]/input', result)
            await click(driver, 30, '//*[@id="f_log"]/table[2]/tbody/tr[2]/td[1]/input')

            await asyncio.sleep(5.5)
    except:
        pass

    try:
        await click(driver, 30, '//label[@for="USDTTRC"]')
        await click(driver, 30, '//input[@value="Сделать платеж"]')
    except Exception as e:
        print(f'ERROR MAKE PAYMENT \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="auth"]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="auth"]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]', timeout=30)
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
