from time import sleep
from flask import Flask
from flask import jsonify
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path
from selenium.webdriver.common.keys import Keys

#CONSTANS

app = Flask(__name__)
url = 'https://tier1.shop'
user_login = 'kiracase34@gmail.com'

#CHROME OPTIONS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")

#driver = webdriver.Chrome(options=options)

def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        driver.maximize_window()

        try:
            driver.implicitly_wait(10)
            pay_tariff = driver.find_element(By.CSS_SELECTOR, 'div.elementor-element.elementor-element-70067fc.uael-add-to-cart-align-center.elementor-widget.elementor-widget-uael-woo-add-to-cart > div > div > a')
            driver.execute_script("arguments[0].click();", pay_tariff)
        except Exception as e:
            print(f"PAY BUTTON TARIFF ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_tariff = driver.find_element(By.CSS_SELECTOR, 'div.cart-collaterals > div.cart_totals > div > a')
            driver.execute_script("arguments[0].click();", choose_tariff)
        except Exception as e:
            print(f"CHOOSE TARIFF ERROR \n{e}")

        try:
            sleep(3)
            driver.implicitly_wait(10)
            input_name = driver.find_element(By.ID, 'billing_first_name')
            input_name.send_keys("Kira")

            driver.implicitly_wait(10)
            input_email_step1 = driver.find_element(By.ID, 'billing_email')
            input_email_step1.send_keys(user_login)
        except Exception as e:
            print(f'INPUT DATA ERROR \n{e}')

        try:
            driver.implicitly_wait(10)
            choose_cryptadium = driver.find_element(By.ID, 'payment_method_cryptadium')
            driver.execute_script("arguments[0].click();", choose_cryptadium)
        except Exception as e:
            print(f"CHOOSE CRYPTADIUM ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            ticket_click = driver.find_element(By.ID, 'terms')
            driver.execute_script("arguments[0].click();", ticket_click)
        except Exception as e:
            print(f'TICKER ERROR \n{e}')

        #Подтвердить заказ
        try:
            driver.implicitly_wait(10)
            accept_button = driver.find_element(By.ID, 'place_order')
            driver.execute_script("arguments[0].click();", accept_button)
        except Exception as e:
            print(f"ACCEPT BUTTON ERROR \n{e}")

        try:
            sleep(2)
            driver.implicitly_wait(5)
            step_to_pay = driver.find_element(By.ID, 'redirectButton')
            driver.execute_script("arguments[0].click();", step_to_pay)
        except Exception as e:
            print(f"Запрос был создан")

            try:
                sleep(3)
                driver.implicitly_wait(10)
                input_email = driver.find_element(By.ID, 'Email')
                input_email.send_keys(user_login)
            except Exception as e:
                print(f"INPUT EMAIL ERROR \n{e}")

            try:
                driver.implicitly_wait(10)
                ticket_accept_email = driver.find_element(By.CSS_SELECTOR, 'div.order_info > div.form_bottom > label > div')
                driver.execute_script("arguments[0].click();", ticket_accept_email)

                driver.implicitly_wait(10)
                buy_ = driver.find_element(By.CSS_SELECTOR, 'div.order_info > div.form_bottom > button')
                driver.execute_script("arguments[0].click();", buy_)
            except Exception as e:
                print(f"ACCEPT ERROR \n{e}")

            try:
                sleep(2)
                driver.implicitly_wait(10)
                accept_submit = driver.find_element(By.CSS_SELECTOR, '#payment-form > div.active.confirm > button')
                driver.execute_script("arguments[0].click();", accept_submit)
            except Exception as e:
                print(f"OK BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR, 'div.payment_requisites > div.req_to_clipboard_wrapper > div > p').text

            driver.implicitly_wait(10)
            amount = driver.find_element(By.CSS_SELECTOR, 'div.payment_req > div > div.payment_requisites > div.req_to_clipboard > p').text

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
