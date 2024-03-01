from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_argument("--headless")
options.headless = False

#CONSTANS

url = 'https://infoshopik.com/shop/aleksej-chechukevich-denezhnaja-mashina-2024/'
user_login = "kiracase34@gmail.com"
user_password = ""


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        driver.maximize_window()

        try:
            driver.implicitly_wait(10)
            buy_one_click_button = driver.find_element(By.CSS_SELECTOR, 'form > button.single_add_to_cart_button.clickBuyButton.button21.button.alt.ld-ext-left')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_one_click_button)
        except Exception as e:
            print(f"BUY ONE CLICK BUTTON ERROR \n{e}")


        try:
            driver.implicitly_wait(10)
            input_email = driver.find_element(By.CSS_SELECTOR, '#billing_email')
            sleep(2)
            input_email.clear()
            input_email.send_keys(user_login)
        except Exception as e:
            print(f"INPUT EMAIL ERROR \n{e}")

        print("Step 1 skip")

        try:
            driver.implicitly_wait(10)
            place_order = driver.find_element(By.ID, 'place_order')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", place_order)
        except Exception as e:
            print(f"PLACE ORDER \n{e}")

        print("Step 2 skip")

        try:
            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.CSS_SELECTOR, 'div.row.g-2.mb-3.animate__animated.animate__fadeIn > div:nth-child(13) > div > div')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")

        print("Step 3 skip")

        try:
            driver.implicitly_wait(10)
            input_email_step2 = driver.find_element(By.ID, 'email')
            input_email_step2.clear()
            input_email_step2.send_keys(user_login)

            driver.implicitly_wait(10)
            button_buy = driver.find_element(By.CSS_SELECTOR, '#createForm > div.d-flex.flex-md-row.flex-column.mb-3 > button.btn.btn-primary.btn-sign.me-md-2.mb-2.mb-md-0 > span:nth-child(1)')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", button_buy)
        except Exception as e:
            print(f"INPUT AND ACCEPT ERROR \n{e}")

        print("Step 4 skip")

        try:
            driver.implicitly_wait(30)
            address = driver.find_element(By.ID,'address').get_attribute('value')

            driver.implicitly_wait(30)
            amount = driver.find_element(By.ID,'amount').get_attribute('value')

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }

        except Exception as e:
            print(f"DATA ERROR \n{e}")
            return None


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
