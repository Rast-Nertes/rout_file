from time import sleep
from flask import Flask
from flask import jsonify
#from selenium import webdriver
from fake_useragent import UserAgent
from seleniumwire import webdriver
#import undetected_chromedriver2 as uc2
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#CONSTANS

app = Flask(__name__)
url = 'https://arbitragescanner.io/'
user_login = 'kiracase34@gmail.com'
user_first_name = 'kiraa'
user_last_name = 'Ivanova'

#CHROME OPTIONS

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--disable-save-password-bubble")

user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")

#driver = webdriver.Chrome(options=options)

def get_wallet():
    try:
        with webdriver.Chrome(options=options) as driver:
            driver.get('https://nowvcc.com/p/amazon-aws-vcc/')
            driver.maximize_window()
            driver.execute_script("window.scrollBy(0, 350);")

            try:
                add_to_cart = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="product-639"]/div[2]/form/button'))
                )
                add_to_cart.click()
            except Exception as e:
                print(f"ADD TO CART ERROR \n{e}")

            driver.get('https://nowvcc.com/checkout/')

            try:
                email_input = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="billing_email"]'))
                )
                email_input.send_keys(user_login)
                sleep(1)
                first_name = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="billing_first_name"]'))
                )
                first_name.send_keys(user_first_name)
                sleep(1)
                second_name = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="billing_last_name"]'))
                )
                second_name.send_keys(user_last_name)
            except Exception as e:
                print(f"INPUT ERROR \n{e}")

            try:
                continue_to_payment = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="cfw-customer-info-action"]/a[2]'))
                )
                continue_to_payment.click()
            except Exception as e:
                print(f"CONTINUE BUTTON ERROR \n{e}")

            try:
                choose_wallet = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="payment"]/ul/li[5]/div'))
                )
                choose_wallet.click()
            except Exception as e:
                print(f"CHOSOE WALLET ERROR \n{e}")

            driver.execute_script("window.scrollBy(0, 350);")

            try:
                continue_ = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="place_order"]'))
                )
                continue_.click()
            except Exception as e:
                print(f"CONTINUE WALLET ERROR \n{e}")

            try:
                usdt_trc20 = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="__layout"]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div[2]'))
                )
                usdt_trc20.click()
            except Exception as e:
                print(f"CHOOSE TRC20 ERROR \n{e}")

            amount = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="__layout"]/div/div/div/div/div[1]/div/div[7]/div[1]/div[2]/span[1]'))
            )
            amount = amount.text

            address = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="__layout"]/div/div/div/div/div[2]/div[1]/div[5]/div[1]/div/div[1]/div[4]/span'))
            )
            address = address.text
            # except Exception as e:
            #   print(f"AMOUNT ERROR \n{e}")

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }

    except Exception as e:
        print(f"GET WALLET ERROR \n{e}")
        return None

@app.route('/api/selenium/nowvcc')
def wallet():
    wallet_data = get_wallet()
    #print(wallet_data)
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5020)
    #wallet()
