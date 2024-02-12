import requests
from PIL import Image
import pytesseract
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
url = 'https://www.tabproxy.com/login'
user_login = 'kiracase34@gmail.com'
user_password = 'npvNPV'

#CHROME CONSTANS

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False
chrome_options.add_argument('--disable-save-password-bubble')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

user_agent = UserAgent()
chrome_options.add_argument(f"user-agent={user_agent.random}")

#driver = webdriver.Chrome(options=chrome_options)


def login(driver):
    try:
        driver.get('https://www.5gold.com/login.html')
        driver.maximize_window()
        try:
            login_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="lemail"]'))
            )
            login_input.send_keys(user_login)
        except Exception as e:
            print(f"LOGIN INPUT ERROR \n{e}")

        try:
            password_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="lpassword"]'))
            )
            password_input.send_keys(user_password)
        except Exception as e:
            print(f"PASSWORD INPUT ERROR \n{e}")

        log_in = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="bttlogin"]'))
        )
        log_in.click()

    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

def get_wallet_data():
    try:
        with webdriver.Chrome(options=chrome_options) as driver:
            login(driver)
            sleep(2)
            driver.get('https://www.5gold.com/final-fantasy-xiv-gil/eu-cerberus')

            driver.execute_script("window.scrollBy(0, 250);")
        #<a href="/orderpay.html" class="btn btn-upper btn-primary btn-block m-t-20">Checkout</a>
            try:
                add_to_cart = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="ProductList"]/li[1]/div[3]/button'))
                )
                add_to_cart.click()
            except Exception as e:
                print(f"ADD TO CART ERROR -- \n{e}")
            sleep(2)
            driver.get('https://www.5gold.com/orderpay.html')
            driver.execute_script("window.scrollBy(0, 400);")

            driver.find_element(By.XPATH, '//*[@id="iEmail"]').send_keys(user_login)
            driver.execute_script("window.scrollBy(0, 600);")

            try:
                choose_crypto_pay = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="checkoutform"]/div[6]/table/tbody/tr[1]/td/ul/li[4]/label/img'))
                )
                choose_crypto_pay.click()
            except Exception as e:
                print(f"COINPAL ERROR \n{e}")

            driver.execute_script("window.scrollBy(0, 250);")

            try:
                pay_now = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="checkout_button_continue"]'))
                )
                pay_now.click()
                #Слип, чтобы подождать прогрузки всплывающего окна
                sleep(5)
                pay_now.send_keys(Keys.ENTER)
            except Exception as e:
                pass

            try:
                usdt_trc20 = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div[2]'))
                )
                usdt_trc20.click()
            except Exception as e:
                print(f"CHOOSE TRC20 ERROR \n{e}")


            amount = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div/div/div/div[1]/div/div[7]/div[1]/div[2]/span[1]'))
            )
            amount = amount.text

            address = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div/div/div/div[2]/div[1]/div[5]/div[1]/div/div[1]/div[4]/span'))
            )
            address = address.text
            #except Exception as e:
            #   print(f"AMOUNT ERROR \n{e}")

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
    except Exception as e:
        print(f"GET WALLET ERROR \n{e}")
        return None

@app.route('/api/selenium/5gold')
def wallet():
    wallet_data = get_wallet_data()
    #print(wallet_data)
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5019)