import requests
from time import sleep
from flask import Flask
from flask import jsonify
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#CONSTANS

app = Flask(__name__)
url = ''
user_login = 'kiracase34@gmail.com'
user_first_name = 'kiraa'
user_last_name = 'Ivanova'

#CHROME CONSTANS

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False
chrome_options.add_argument('--disable-save-password-bubble')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

user_agent = UserAgent()
chrome_options.add_argument(f"user-agent={user_agent.random}")

#driver = webdriver.Chrome(options=chrome_options)


def get_wallet():
    try:
        with webdriver.Chrome(options=chrome_options) as driver:

            driver.get('https://shopvcc.com/shop/')
            driver.maximize_window()

            driver.execute_script("window.scrollBy(0, 350);")

            try:
                add_to_cart = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/div/ul/li[4]/div[2]/a[2]'))
                )
                add_to_cart.click()
                sleep(5)
            except Exception as e:
                print(f"ADD TO CART ERROR \n{e}")

            #Проскроллить в верх
            driver.execute_script("window.scrollTo(0, 0);")

            try:
                busket = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/section[3]/div/div/div/section/div/div[3]/div/div/div/div/div/div[2]/a'))
                )
                busket.click()
            except Exception as e:
                print(f"BUSKET ERROR \n{e}")

            try:
                checkout = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="page"]/div[1]/section[3]/div/div/div/section/div/div[3]/div/div/div/div/div/div[1]/div/div[2]/div[3]/a[2]'))
                )
                checkout.click()
            except Exception as e:
                print(f"CHECHOUT ERROR \n{e}")

            driver.execute_script("window.scrollTo(0, 500);")

            try:
                input_first_name = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="billing_first_name"]'))
                )
                input_first_name.clear()
                input_first_name.send_keys(user_first_name)

                input_last_name = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="billing_last_name"]'))
                )
                input_last_name.clear()
                input_last_name.send_keys(user_last_name)

                input_email = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="billing_email"]'))
                )
                input_email.clear()
                input_email.send_keys(user_login)

            except Exception as e:
                print(f"INPUT NAME`S ERROR \n{e}")

            try:
                continue_to_payment = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="place_order"]'))
                )
                continue_to_payment.click()
            except Exception as e:
                print(f"CONTINUE TO PAYMENT \n{e}")


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

@app.route('/api/selenium/shopvccv1')
def wallet():
    wallet_data = get_wallet()
    #print(wallet_data)
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5021)
    #wallet()