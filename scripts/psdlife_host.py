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

url = 'https://psdlife.com/product/albania-id-card-psd-template-physical-appearance-of-the-biometric-id/'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        driver.maximize_window()

        try:
            driver.implicitly_wait(40)
            add_to_cart_button = driver.find_element(By.CSS_SELECTOR, 'div > div.summary.entry-summary.col-md-7 > form > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", add_to_cart_button)

            sleep(2)
            driver.get('https://psdlife.com/checkout/')

            driver.implicitly_wait(30)
            proceed_to_check = driver.find_element(By.CSS_SELECTOR, '#panel-cart-total > div > div > a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", proceed_to_check)
        except Exception as e:
            print(f"ERROR ADD CART \n{e}")

        try:
            driver.implicitly_wait(20)
            input_first_name = driver.find_element(By.ID, 'billing_first_name')
            input_first_name.clear()
            input_first_name.send_keys("Kira")

            driver.implicitly_wait(20)
            input_last_name = driver.find_element(By.ID, 'billing_last_name')
            input_last_name.clear()
            input_last_name.send_keys('Ivanova')

            driver.implicitly_wait(20)
            input_email = driver.find_element(By.ID, 'billing_email')
            input_email.send_keys(user_email)
        except Exception as e:
            print(f"DATA ERROR \n{e}")

        try:
            driver.implicitly_wait(30)
            place_order = driver.find_element(By.ID, 'place_order')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", place_order)
        except Exception as e:
            print(f"ERROR HOST \n{e}")

        try:
            driver.implicitly_wait(30)
            amount = driver.find_element(By.CSS_SELECTOR, 'div > div.mcc.online_payment_instructions.mycryptocheckout > div > p > span.amount > span > input').get_attribute('value').replace('USDT_TRON', '').replace(' ', '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR, 'div > div.mcc.online_payment_instructions.mycryptocheckout > div > p > span.to > span > input').get_attribute('value')

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
