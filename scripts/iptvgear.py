from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://iptvgear.org'
user_login = "kiracase34@gmail.com"

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

#API CONSTANS

api_key = '7f728c25edca4f4d0e14512d756d6868'

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        driver.maximize_window()

        try:
            driver.implicitly_wait(10)
            choose_tariff = driver.find_element(By.CSS_SELECTOR, '#pricing > div:nth-child(2) > div > div > div > div > ul > li.footer > a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_tariff)
        except Exception as e:
            print(f"CHOOSE TARIFF ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            continue_button = driver.find_element(By.ID, 'button-account')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button)
        except Exception as e:
            print(f"CONTINUE BUTTON \n{e}")

        try:
            driver.implicitly_wait(10)
            select_connection = driver.find_element(By.CSS_SELECTOR, '#input-payment-custom-field1 > option:nth-child(1)')
            sleep(2)
            driver.execute_script("arguments[0].remove();", select_connection)
        except Exception as e:
            print(f"CONNECTIONS ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_first_name = driver.find_element(By.ID, 'input-payment-firstname')
            input_first_name.clear()
            sleep(1)
            input_first_name.send_keys("Kira")

            driver.implicitly_wait(10)
            input_last_name = driver.find_element(By.ID, 'input-payment-lastname')
            input_last_name.clear()
            sleep(1)
            input_last_name.send_keys("Ivanova")

            driver.implicitly_wait(10)
            input_email = driver.find_element(By.ID, 'input-payment-email')
            input_email.clear()
            sleep(1)
            input_email.send_keys(user_login)
        except Exception as e:
            print(f"INPUT ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            continue_button_2 = driver.find_element(By.ID, 'button-guest')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button_2)
        except Exception as e:
            print(f"CONTINUE BUTTON STEP2 ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            ticket = driver.find_element(By.CSS_SELECTOR, 'div > div.buttons > div > input[type=checkbox]:nth-child(2)')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", ticket)
        except Exception as e:
            print(f"TICKET ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            continue_button_3 = driver.find_element(By.ID, 'button-payment-method')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button_3)
        except Exception as e:
            print(f"CONTINUE BUTTON STEP3 ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            confirm_order = driver.find_element(By.CSS_SELECTOR, '#collapse-checkout-confirm > div > div.buttons > div.pull-right > a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", confirm_order)
        except Exception as e:
            print(f"CONFIRM ORDER ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            select_currency = driver.find_element(By.CSS_SELECTOR, 'div.invoice__steps > div.choose-currency-step > div.currencies-select > div')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", select_currency)

            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.CSS_SELECTOR, 'div.currencies-dropdown.currencies-select__body.currencies-select__body_animate > div.currencies-dropdown__content > ul > li:nth-child(2)')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(10)
            next_step = driver.find_element(By.CSS_SELECTOR, 'div.invoice__content > div.invoice__steps > div.choose-currency-step > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step)
        except Exception as e:
            print(f"SELECT TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, 'div.send-deposit-step__body > div.send-deposit-step__info > div:nth-child(1) > div.payment-info-item__content > div > div.copy-text__box').text.replace("USDT", '').replace(" ", '').replace("\nTRX", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR, 'div.invoice__steps > div.send-deposit-step > div.send-deposit-step__body > div.send-deposit-step__info > div:nth-child(2) > div.payment-info-item__content > div > div.copy-text__box').text

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
