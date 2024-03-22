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

url = 'https://blankpsd.com/product/ohio-drivers-license-template/?doing_wp_cron=1709210338.6194310188293457031250'
user_login = "kiracase34@gmail.com"
user_password = "ErJYGKiG7w2fGTF"

# CHROME CONSTANS

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
            driver.implicitly_wait(15)
            add_to_cart_button = driver.find_element(By.CSS_SELECTOR, 'div.product-info.summary.col-fit.col.entry-summary.product-summary > form > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", add_to_cart_button)
        except Exception as e:
            print(f"ADD TO CART ERROR \n{e}")

        driver.get('https://blankpsd.com/checkout/')

        try:
            sleep(5)
            driver.implicitly_wait(10)
            place_order_button = driver.find_element(By.CSS_SELECTOR, '#payment > ul > li.wc_payment_method.payment_method_wapg_altcoin_payment > label')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", place_order_button)
        except Exception as e:
            print(f"PLACE ORDER ERROR \n{e}")

        try:
            driver.implicitly_wait(15)
            input_first_name = driver.find_element(By.ID, 'billing_first_name')
            input_first_name.clear()
            input_first_name.send_keys("Kira")

            driver.implicitly_wait(15)
            input_last_name = driver.find_element(By.ID, 'billing_last_name')
            input_last_name.clear()
            input_last_name.send_keys("Ivanova")

            driver.implicitly_wait(10)
            input_email = driver.find_element(By.ID, 'billing_email')
            input_email.clear()
            input_email.send_keys(user_login)
        except Exception as e:
            print(f"INPUT DATA ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            select_coin = driver.find_element(By.ID, 'CsaltCoin')
            sleep(5)
            #driver.execute_script("arguments[0].click();", select_coin)
            select_coin.click()

            sleep(1.5)
            for _ in range(2):
                actions.send_keys(Keys.ARROW_DOWN).perform()
                sleep(0.5)

            actions.send_keys(Keys.ENTER).perform()
        except Exception as e:
            print(f"SELECT ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, '#wapg_order_review > table > tfoot > tr.cart-subtotal > td > span').text.replace("-", "").replace(" ", '').replace("Tether(USDT)", "")


            driver.implicitly_wait(10)
            address = driver.find_element(By.ID, 'alt-coinAddress').get_attribute('value')

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
