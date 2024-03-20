from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://aslitheme.com/accountpage/'
user_email = "kiracase34@gmail.com"
user_password = "qvFE6ikwaPYj9xw"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.ID, 'username')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.ID, 'password')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'div.u-column1.col-1 > form > p:nth-child(3) > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
        #Залогиниться
        sleep(7.5)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    sleep(2)
    driver.get('https://aslitheme.com/product/zambia-driver-license-psd-template/')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(10)
            add_to_cart_button = driver.find_element(By.CSS_SELECTOR, 'div.summary.entry-summary > form > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", add_to_cart_button)
        except Exception as e:
            print(f"ADD TO CART BUTTON ERROR \n{e}")

        sleep(5)
        driver.get('https://aslitheme.com/cartpage/')

        try:
            driver.implicitly_wait(10)
            input_count = driver.find_element(By.XPATH, '/html/body/div[1]/main/article/div/div/form/table/tbody/tr[1]/td[5]/div/input')
            input_count.clear()
            input_count.send_keys('1')

            driver.implicitly_wait(10)
            update_cart = driver.find_element(By.CSS_SELECTOR, 'form > table > tbody > tr:nth-child(2) > td > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", update_cart)
            sleep(2)

            driver.implicitly_wait(10)
            proceed_to_checkout_button = driver.find_element(By.CSS_SELECTOR, 'div > div.cart-collaterals > div > div > a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", proceed_to_checkout_button)
        except Exception as e:
            print(f"PROCEED TO CHECKOUT ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_nowpayments = driver.find_element(By.CSS_SELECTOR, '#payment > ul > li.wc_payment_method.payment_method_nowpayments_gateway > label')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_nowpayments)
            sleep(4)
        except Exception as e:
            print(f"ERROR CHOOSE NOWPAYMENTS \n{e}")

        try:
            driver.implicitly_wait(10)
            place_order = driver.find_element(By.ID, 'place_order')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", place_order)
        except Exception as e:
            print(f"ERROR PLACE ORDER \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_wallet = driver.find_element(By.CSS_SELECTOR, 'div.invoice__content > div.invoice__steps > div.choose-currency-step > div.currencies-select > div')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_wallet)

            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.CSS_SELECTOR, 'div.currencies-select > div.currencies-dropdown.currencies-select__body.currencies-select__body_animate > div.currencies-dropdown__content > ul > li:nth-child(11)')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            next_step_button = driver.find_element(By.CSS_SELECTOR, 'div.invoice__steps > div.choose-currency-step > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step_button)
        except Exception as e:
            print(f"ERROR NEXT STEP BUTTON \n{e}")

        try:
            driver.implicitly_wait(10)
            amount = driver.find_element(By.CSS_SELECTOR, 'div.send-deposit-step__body > div.send-deposit-step__info > div:nth-child(1) > div.payment-info-item__content > div > div.copy-text__box').text.replace('USDT', '').replace(" ", '').replace('TRX', '').replace('\n', '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR, 'div.send-deposit-step > div.send-deposit-step__body > div.send-deposit-step__info > div:nth-child(2) > div.payment-info-item__content > div > div.copy-text__box').text

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
