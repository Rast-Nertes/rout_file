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

url = 'https://blankpsd.com/product/cameroon-passport-psd-template/'
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
            driver.implicitly_wait(30)
            sleep(6)
            add_to_cart_button = driver.find_element(By.XPATH, '(//button[@type="submit"])[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", add_to_cart_button)
        except Exception as e:
            return {"status":"0", "ext":f"error add to cart {e}"}

        sleep(5)
        driver.get('https://blankpsd.com/checkout/')

        while True:
            try:
                sleep(3.5)
                driver.implicitly_wait(10)
                place_order_button = driver.find_element(By.CSS_SELECTOR, '#payment > ul > li.wc_payment_method.payment_method_wapg_altcoin_payment > label')
                sleep(1.5)
                driver.execute_script("arguments[0].click();", place_order_button)
            except Exception as e:
                return {"status":"0", "ext":f"error place order {e}"}

            try:
                sleep(5)
                driver.implicitly_wait(20)
                select_coin = driver.find_element(By.ID, 'CsaltCoin')
                sleep(5)
                select_coin.click()

                sleep(1.5)
                for _ in range(2):
                    actions.send_keys(Keys.ARROW_DOWN).perform()
                    sleep(0.5)

                actions.send_keys(Keys.ENTER).perform()
            except Exception as e:
                return {"status": "0", "ext":f"error select {e}"}

            try:

                driver.implicitly_wait(10)
                amount = driver.find_element(By.CSS_SELECTOR, '#wapg_order_review > table > tfoot > tr.cart-subtotal > td > span').text.replace("-", "").replace(" ", '').replace("Tether(USDT)", "")

                driver.implicitly_wait(10)
                address = driver.find_element(By.ID, 'alt-coinAddress').get_attribute('value')

                return {
                    "address": address,
                    "amount": amount,
                    "currency": "usdt"
                }
            except Exception as e:
                print(f"DATA ERROR ")
                driver.refresh()
                continue


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
