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

url = 'https://www.otviptv.com/product/subscription-iptv-1-month-otv-iptv/'
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
        actions = ActionChains(driver)

        driver.get(url)
        driver.maximize_window()

        try:
            driver.implicitly_wait(10)
            select_format = driver.find_element(By.ID, 'select-format')
            sleep(5)
            select_format.click()

            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.5)
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.5)
            actions.send_keys(Keys.ENTER).perform()
            sleep(0.5)
        except Exception as e:
            print(f"SELECT ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            buy_now_button = driver.find_element(By.CSS_SELECTOR, 'div.woocommerce-variation-add-to-cart.variations_button.woocommerce-variation-add-to-cart-enabled > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_now_button)
        except Exception as e:
            print(f"BUY NOW BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_first_name = driver.find_element(By.ID, 'billing_first_name')
            input_first_name.clear()
            input_first_name.send_keys("Kira")

            driver.implicitly_wait(10)
            input_last_name = driver.find_element(By.ID, 'billing_last_name')
            input_last_name.clear()
            input_last_name.send_keys("Ivanova")

            driver.implicitly_wait(10)
            address_input = driver.find_element(By.ID, 'billing_address_1')
            address_input.clear()
            address_input.send_keys("111")

            driver.implicitly_wait(10)
            city_input = driver.find_element(By.ID, 'billing_city')
            city_input.clear()
            city_input.send_keys("City")
        except Exception as e:
            print(f"INPUT MAIN DATA ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_zipcode = driver.find_element(By.ID, 'billing_postcode')
            input_zipcode.clear()
            input_zipcode.send_keys("12312")
        except Exception as e:
            print(f"INPUT ZIPCODE ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_phone = driver.find_element(By.ID, 'billing_phone')
            input_phone.clear()
            input_phone.send_keys("+11122233311")

            driver.implicitly_wait(10)
            input_email = driver.find_element(By.ID, 'billing_email')
            input_email.clear()
            input_email.send_keys("kiracase34@gmail.com")
        except Exception as e:
            print(f"INPUT PHONE AND EMAIL ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            ticket = driver.find_element(By.ID, 'terms')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", ticket)

            driver.implicitly_wait(10)
            place_order = driver.find_element(By.ID, 'place_order')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", place_order)
        except Exception as e:
            print(f"PLACE ORDER ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.CSS_SELECTOR, '#__layout > div > div > div > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2)')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            amount = driver.find_element(By.CSS_SELECTOR, '#__layout > div > div > div > div > div:nth-child(1) > div > div.order_total > div:nth-child(1) > div.goods_total_value > span.total_span.total_span_blue').text

            driver.implicitly_wait(10)
            sleep(5)
            address = driver.find_element(By.CSS_SELECTOR, '#__layout > div > div > div > div > div:nth-child(2) > div:nth-child(1) > div.payment_box > div:nth-child(1) > div > div.payment_info > div:nth-child(4)').text

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
