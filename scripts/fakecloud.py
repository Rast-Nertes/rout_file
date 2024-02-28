from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://fake-cloud.com/product/uzbekistan-passport-psd-template/'
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
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        driver.get(url)
        driver.maximize_window()
    
        try:
            driver.implicitly_wait(10)
            buy_now_button = driver.find_element(By.CSS_SELECTOR, 'form > div > button.single_add_to_cart_button.ajax_add_to_cart.button.alt.button-buy-now')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_now_button)
        except Exception as e:
            print(f"BUY BUTTON ERROR \n{e}")
    
        try:
            driver.implicitly_wait(10)
            input_email = driver.find_element(By.ID, 'billing_email')
            sleep(1)
            input_email.clear()
            input_email.send_keys(user_login)
        except Exception as e:
            print(f"INPUT EMAIL ERROR \n{e}")
    
        try:
            driver.implicitly_wait(10)
            choose_paymentars_method = driver.find_element(By.ID, 'payment_method_nowpayments')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_paymentars_method)
    
            driver.implicitly_wait(10)
            place_order_button = driver.find_element(By.ID, 'place_order')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", place_order_button)
            sleep(3)
            driver.refresh()
        except Exception as e:
            print(f"PAYMENTRS ACTION ERROR \n{e}")
    
        try:
            driver.implicitly_wait(30)
            choose_currency = driver.find_element(By.CSS_SELECTOR, 'div.invoice__steps > div.choose-currency-step > div.currencies-select > div')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_currency)
    
            driver.implicitly_wait(10)
            choose_usdt_trc20 = driver.find_element(By.CSS_SELECTOR, 'div.currencies-dropdown.currencies-select__body.currencies-select__body_animate > div.currencies-dropdown__content > ul > li:nth-child(2)')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_usdt_trc20)
        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")
    
        try:
            driver.implicitly_wait(30)
            next_step_button = driver.find_element(By.CSS_SELECTOR, 'div.invoice__content > div.invoice__steps > div.choose-currency-step > button')
            sleep(3)
            driver.execute_script("arguments[0].click();", next_step_button)
        except Exception as e:
            print(f"NEXT STEP BUTTON ERROR \n{e}")
    
        try:
            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR,
                                         'div.send-deposit-step__body > div.send-deposit-step__info > div:nth-child(1) > div.payment-info-item__content > div > div.copy-text__box').text.replace(
                "USDT", '').replace(" ", '').replace("\nTRX", '')
    
            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR,
                                          'div.invoice__steps > div.send-deposit-step > div.send-deposit-step__body > div.send-deposit-step__info > div:nth-child(2) > div.payment-info-item__content > div > div.copy-text__box').text
    
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
