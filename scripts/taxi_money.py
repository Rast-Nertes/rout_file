from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://www.taxi-money.ink/login'
user_email = "alex37347818@gmail.com"
user_password = "qwe123asd"

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

#PROXY_CONSTANS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@45.130.254.133:8000",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def solve_captcha():
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key("6ab87383c97cb688c42b47e81c96bbcc")
    solver.set_website_url(url)
    solver.set_website_key("6Lf9fN0hAAAAAB1ZlI0Js8-_iUMl2EfxnsylYvR3")

    solver.set_soft_id(0)
    g_response = solver.solve_and_return_solution()
    if g_response != 0:
        print("g-response: " + g_response)
    else:
        print("task finished with error " + solver.error_code)

    return g_response


def login(driver):
    driver.get(url)
    try:
        driver.implicitly_wait(10)
        textarea = driver.find_element(By.TAG_NAME, 'textarea')

        #Время на загрузку капчи
        sleep(7.5)
        driver.execute_script("arguments[0].removeAttribute('style');", textarea)
        solved_task = solve_captcha()

        textarea.clear()
        textarea.send_keys(solved_task)
    except Exception as e:
        print(f"REVERSE TEXTAREA ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        input_login = driver.find_element(By.CSS_SELECTOR, 'div.lpContent > form > div.formRow.loginRow > input[type=text]')
        input_login.clear()
        input_login.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'div.lpContent > form > div.formRow.passwordRow > input[type=password]')
        input_password.clear()
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"INPUT DATA ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'div.lpContent > form > div.formRow.submitRow > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN BUTTON ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        driver.maximize_window()
        login(driver)
        sleep(3)
        driver.get('https://www.taxi-money.ink/finance?p=1000#deposit')

        try:
            driver.implicitly_wait(10)
            choose_crypto_payment = driver.find_element(By.CSS_SELECTOR, 'form > div > div.form-group.row > div > div > div > div > div:nth-child(22) > div > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_crypto_payment)

            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.CSS_SELECTOR, 'form > div > div.form-group.row > div > div > div > div > div:nth-child(3) > div > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            submit_button = driver.find_element(By.CSS_SELECTOR, 'div.panel-content.finance-content > form > div > div:nth-child(8) > div > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit_button)
        except Exception as e:
            print(f"SUBMIT BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(40)
            address = driver.find_element(By.CSS_SELECTOR, 'section > div.flex.w-full.flex-col.justify-center.gap-4.sm\:flex-row.sm\:gap-6 > div.flex.h-\[312px\].w-full.flex-col.gap-5.rounded-xl.border.border-\[\#E5E7EB\].p-5.sm\:p-6.sm\:w-\[55\%\] > div:nth-child(3) > div > button').get_attribute("value")

            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, 'section > div.flex.w-full.flex-col.justify-center.gap-4.sm\:flex-row.sm\:gap-6 > div.flex.h-\[312px\].w-full.flex-col.gap-5.rounded-xl.border.border-\[\#E5E7EB\].p-5.sm\:p-6.sm\:w-\[55\%\] > div.flex.flex-col.gap-2 > span.block.text-xl.font-bold.false').text.replace("USDT", "").replace(" ", "")

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
