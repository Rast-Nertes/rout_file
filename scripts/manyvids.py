import asyncio
import pyautogui
from flask import jsonify
from anticaptchaofficial.recaptchav3proxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

#iframe - 6LdvaGAbAAAAAMN8oihinZHd52w7nwFif_FbUAql
#v2 - 6LdVXCkTAAAAAIHqCBdOu-UdxiFm9-BxCVRYhMgY
#v3 - 6LdvaGAbAAAAAMN8oihinZHd52w7nwFif_FbUAql


url = 'https://www.manyvids.com/Login/'
user_email = "rwork875@gmail.com"
user_password = "66447722r"
api_ = '7f728c25edca4f4d0e14512d756d6868'

# CHROME CONSTANS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

# with open('config.txt') as file:
#     paths = file.readlines()
#     chrome_path = paths[0].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
# options.add_argument("--auto-open-devtools-for-tabs")
# options.binary_location = chrome_path


def solve_captcha():
    solver = recaptchaV3Proxyless()
    solver.set_verbose(1)
    solver.set_key("6ab87383c97cb688c42b47e81c96bbcc")
    solver.set_website_url("https://www.manyvids.com/Login/")
    solver.set_website_key("6LdvaGAbAAAAAMN8oihinZHd52w7nwFif_FbUAql")
    solver.set_page_action("Signup")
    solver.set_min_score(0.6)

    solver.set_soft_id(0)

    g_response = solver.solve_and_return_solution()
    return g_response


async def login(driver):
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    sleep(2)
    await driver.get(url, timeout=60)
    await driver.set_window_size(1400, 800)

    result_captcha = solve_captcha()
    input_captcha_code = await driver.find_element(By.TAG_NAME, 'textarea', timeout=10)
    await driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)

    try:
        input_email = await driver.find_element(By.ID, 'triggerUsername', timeout=20)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.ID, 'triggerPassword', timeout=20)
        await input_pass.write(user_password)
    except Exception as e:
        print(f"ERROR INPUT DATA \n{e}")

    try:
        log_button = await driver.find_element(By.ID, 'loginAccountSubmit', timeout=10)
        sleep(1.5)
        await driver.execute_script("arguments[0].click();", log_button)
    except Exception as e:
        print(f"ERROR LOG BUTTON \n{e}")

    await asyncio.sleep(7.5)

    try:
        log_button = await driver.find_element(By.ID, 'loginAccountSubmit', timeout=10)
        sleep(1.5)
        await driver.execute_script("arguments[0].click();", log_button)
    except Exception as e:
        print(f"ERROR LOG BUTTON \n{e}")

    await asyncio.sleep(7.5)
    await driver.get('https://www.manyvids.com/premium/upgrade/')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)
        try:
            choose_tariff = await driver.find_element(By.ID, 'plan-card_button_Subscribe-bottom-1month', timeout=30)
            sleep(2.5)
            await driver.execute_script("arguments[0].click();", choose_tariff)
        except Exception as e:
            print(f"ERROR CHOOSE TARIFF \n{e}")

        try:
            checkout = await driver.find_element(By.ID, 'mvts-checkout-coingate-btn', timeout=20)
            await asyncio.sleep(2)
            await driver.execute_script("arguments[0].click();", checkout)
        except Exception as e:
            print(f'ERROR CHECKOUT BUTTON \n{e}')
        await asyncio.sleep(7.5)
        await driver.clear_proxy()

        try:
            sleep(1.5)
            choose_tether = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div/label[8]', timeout=60)
            await driver.execute_script("arguments[0].click();", choose_tether)

            sleep(1.5)
            continue_button = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/button[1]', timeout=20)
            await driver.execute_script("arguments[0].click();", continue_button)
        except Exception as e:
            print(f"ERROR CHOOSE TETHER \n{e}")

        try:
            input_email = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[1]/form/div/div[2]/input', timeout=30)
            await input_email.click()
            sleep(2.5)
            pyautogui.typewrite(user_email)

            continue_button_2 = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[1]/div[2]/button', timeout=20)
            await driver.execute_script("arguments[0].removeAttribute('disabled')", continue_button_2)
            sleep(1.5)
            await continue_button_2.click()
        except Exception as e:
            print(f"ERROR CONTINUE BUTTON \n{e}")

        try:
            choose_network = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[3]/div/div/label[3]', timeout=20)
            await driver.execute_script("arguments[0].click();", choose_network)

            continue_button_3 = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div[2]/div/button[1]', timeout=20)
            await driver.execute_script("arguments[0].click();", continue_button_3)
        except Exception as e:
            print(f"ERROR CHOOSE NET \n{e}")

        await driver.set_window_size(1000, 700)
        await asyncio.sleep(1.5)

        try:
            amount_elem = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/p', timeout=30)
            amount = await amount_elem.text

            address_elem = await driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[6]/div/div[2]/div/p', timeout=20)
            address = await address_elem.text
            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
