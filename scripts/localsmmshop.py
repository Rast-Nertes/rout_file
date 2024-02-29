from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://localsmmshop.com/product/buy-github-accounts/'
user_login = "kiracase34@gmail.com"
user_password = "kiramira555"

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
            add_to_cart_button = driver.find_element(By.CSS_SELECTOR, 'div.summary.entry-summary > form > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", add_to_cart_button)
        except Exception as e:
            print(f"ERROR ADD TO CART \n{e}")

        driver.get('https://localsmmshop.com/checkout/')

        try:
            driver.implicitly_wait(10)
            input_first_name = driver.find_element(By.ID, 'billing_first_name')
            input_first_name.clear()
            input_first_name.send_keys("Kira")

            driver.implicitly_wait(10)
            input_last_name = driver.find_element(By.ID, 'billing_last_name')
            input_last_name.clear()
            input_last_name.send_keys("Ivanova")
        except Exception as e:
            print(f"INPUT NAMES \n{e}")

        try:
            driver.implicitly_wait(10)
            input_company_name = driver.find_element(By.ID, 'billing_company')
            input_company_name.clear()
            input_company_name.send_keys("Company")

            driver.implicitly_wait(10)
            input_house_number = driver.find_element(By.ID, 'billing_address_1')
            input_house_number.clear()
            input_house_number.send_keys("112")

            driver.implicitly_wait(10)
            input_city = driver.find_element(By.ID, 'billing_city')
            input_city.clear()
            input_city.send_keys("City")
        except Exception as e:
            print(f"INPUT ADDRESS ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_zipcode = driver.find_element(By.ID, 'billing_postcode')
            input_zipcode.clear()
            input_zipcode.send_keys("12312")
        except Exception as e:
            print(f"INPUT ZIPCODE \n{e}")
        try:
            driver.implicitly_wait(10)
            input_number = driver.find_element(By.ID, 'billing_phone')
            input_number.clear()
            input_number.send_keys("+11223311331")
        except Exception as e:
            print(f"INPUT NUMBER ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            input_email = driver.find_element(By.ID, 'billing_email')
            input_email.clear()
            input_email.send_keys(user_login)
        except Exception as e:
            print(f"ERROR INPUT LOGIN \n{e}")

        try:
            driver.implicitly_wait(20)
            place_order_button = driver.find_element(By.ID, 'place_order')
            sleep(6)
            driver.execute_script("arguments[0].click();", place_order_button)
        except Exception as e:
            print(f"ERROR PLACE ORDER BUTTON \n{e}")

        try:
            driver.implicitly_wait(20)
            trc20_network = driver.find_element(By.CSS_SELECTOR, 'div:nth-child(2) > div > div.col-md-6.order-md-2.mt-2 > div > a.a-btn1')
            sleep(2)
            driver.execute_script("arguments[0].click();", trc20_network)
        except Exception as e:
            print(f"TRC20 NETWORK \n{e}")

        try:
            driver.implicitly_wait(20)
            amount = driver.find_element(By.ID, 'amt_val').text

            driver.implicitly_wait(10)
            address = driver.find_element(By.ID, 'add_val').get_attribute('value')

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
