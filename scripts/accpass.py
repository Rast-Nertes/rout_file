#https://www.accpass.store/product/capitalist/
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

url = 'https://www.accpass.store/product/capitalist/'
user_login = "kiracase34@gmail.com"
user_password = "TQOAyI%Kj078"

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        actions = ActionChains(driver)
        driver.get(url)
        driver.maximize_window()

        try:
            driver.implicitly_wait(10)
            add_to_cart_button = driver.find_element(By.CSS_SELECTOR, 'div.add-to-cart-container.form-minimal.is-normal > form > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", add_to_cart_button)
        except Exception as e:
            print(f"ADD TO CART ERROR \n{e}")

        driver.get('https://www.accpass.store/cart/')

        try:
            driver.implicitly_wait(10)
            place_order = driver.find_element(By.CSS_SELECTOR, 'div.cart-container.container.page-wrapper.page-checkout > div > div.woocommerce.row.row-large.row-divided > div.cart-collaterals.large-5.col.pb-0 > div > div.cart_totals > div > a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", place_order)
        except Exception as e:
            print(f"PLACE ORDER BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_email = driver.find_element(By.ID, 'billing_email')
            input_email.clear()
            input_email.send_keys(user_login)
            sleep(4)
        except Exception as e:
            print(f"INPUT EMAIL ERRRO \n{e}")

        try:
            driver.implicitly_wait(20)
            choose_cryptocurrency = driver.find_element(By.CSS_SELECTOR, '#payment > ul > li > div > div > ul > li > span > span.selection > span > span.select2-selection__arrow')
            sleep(2)
            choose_cryptocurrency.click()
            #driver.execute_script("arguments[0].click();", choose_cryptocurrency)
        except Exception as e:
            print(f"CHOOSE CRYPTO CURRENCY ERROR \n{e}")

        for _ in range(4):
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.5)

        actions.send_keys(Keys.ENTER).perform()
        sleep(1)

        try:
            sleep(5)
            driver.implicitly_wait(10)
            accept_place_order = driver.find_element(By.XPATH, '//*[@id="place_order"]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", accept_place_order)
        except Exception as e:
            print(f"ACCEPT PLACE ORDER ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, 'div.large-7.col > div > div > div.ca_payments_wrapper > div.ca_details_box > div.ca_details_text > button > span:nth-child(1) > b').text

            driver.implicitly_wait(20)
            address = driver.find_element(By.CSS_SELECTOR, 'div > div.large-7.col > div > div > div.ca_payments_wrapper > div.ca_details_box > div.ca_details_input > span').text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
