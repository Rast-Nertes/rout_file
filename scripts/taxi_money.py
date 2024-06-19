from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from twocaptcha.solver import TwoCaptcha
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://www.taxi-money.ink/login'
user_email = "alex37347818@gmail.com"
user_password = "qwe123asd"
site_key = '6Lf9fN0hAAAAAB1ZlI0Js8-_iUMl2EfxnsylYvR3'

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

with open('config.txt') as file:
    paths = file.readlines()
    api_key = paths[3].strip()


def captcha_solve():
    solver = TwoCaptcha(api_key)

    result = solver.recaptcha(
        sitekey=site_key,
        url=url
    )

    return result['code']


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    elem_click.click()


def js_click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    driver.execute_script("arguments[0].click();", elem_click)


def wait_visibility(driver, time, XPATH):
    WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.XPATH, XPATH))
    )
    sleep(2.5)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


def login(driver):
    driver.maximize_window()
    driver.get(url)

    try:
        driver.implicitly_wait(10)
        input_login = driver.find_element(By.XPATH, '//input[@name="login"]')
        input_login.clear()
        input_login.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '//input[@name="password"]')
        input_password.clear()
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"INPUT DATA ERROR \n{e}")

    try:
        time_loop = 0
        while True:
            driver.implicitly_wait(10)
            find_check = driver.find_element(By.XPATH, '//div[@class="captcha-solver-info"]').text
            if ("ена" in find_check) or ("lve" in find_check):
                click(driver, 30, '//*[@id="content"]/div/div[2]/div[2]/div/form/div[4]/button')
                break
            else:
                if time_loop > 120:
                    return {"status": "0", "ext": "CAPTCHA ERROR"}
                time_loop += 5
                sleep(5)
                print("Wait 5 seconds, captcha solving...")
    except Exception as e:
        print(f'ERROR CHECKBOX \n{e}')

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
