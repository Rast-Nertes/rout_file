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

url = 'https://smmvcc.com/product/buy-soundcloud-accounts/'
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
            choose_five_accounts = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td > ul > li.variable-item.button-variable-item.button-variable-item-5-soundcloud-accounts > div > span')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_five_accounts)

            driver.implicitly_wait(10)
            buy_now_button = driver.find_element(By.CSS_SELECTOR, 'div.single_variation_wrap > div.woocommerce-variation-add-to-cart.variations_button.woocommerce-variation-add-to-cart-enabled > button.tbay-buy-now.button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_now_button)
        except Exception as e:
            print(f"BUY NOW ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            proceed_button = driver.find_element(By.CSS_SELECTOR, '#main > div > div.cart-collaterals.widget > div > div > a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", proceed_button)
        except Exception as e:
            print(f"PROCEED BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_first_name = driver.find_element(By.ID, 'billing_first_name')
            input_first_name.clear()
            input_first_name.send_keys("Kira")

            driver.implicitly_wait(10)
            input_second_name = driver.find_element(By.ID, 'billing_last_name')
            input_second_name.clear()
            input_second_name.send_keys("Ivanova")
        except Exception as e:
            print(f"INPUT NAMES ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_street_address = driver.find_element(By.ID, 'billing_address_1')
            input_street_address.clear()
            input_street_address.send_keys("111")
        except Exception as e:
            print(f"INPUT STREET ADDRESS ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_phone = driver.find_element(By.ID, 'billing_phone')
            input_phone.clear()
            input_phone.send_keys("+11223311331")

            driver.implicitly_wait(10)
            input_email = driver.find_element(By.ID, 'billing_email')
            input_email.clear()
            input_email.send_keys(user_login)
            sleep(3)
        except Exception as e:
            print(f"INPUT MAIN DATA ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            choose_currency = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/section[2]/div/div/div/div/form[3]/div/div[2]/div/div[2]/div/ul/li[1]/div/p/span')
            choose_currency.click()

            for _ in range(4):
                actions.send_keys(Keys.ARROW_DOWN).perform()
                sleep(0.5)

            actions.send_keys(Keys.ENTER).perform()
        except Exception as e:
            print(f"CHOOSE CURRENCY ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            place_order_button = driver.find_element(By.ID, 'place_order')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", place_order_button)
        except Exception as e:
            print(f"PLACE ORDER ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR,'div.mcc.online_payment_instructions.mycryptocheckout > div > p > span.amount > span > input').get_attribute('value').replace("USDT_TRON", "").replace(" ", "")

            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR, 'div.mcc.online_payment_instructions.mycryptocheckout > div > p > span.to > span > input').get_attribute('value')

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