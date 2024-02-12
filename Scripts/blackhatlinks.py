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
user_login = 'kira34'
user_password = 'лшкфлшкф11'

#CHROME CONSTANS

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False
chrome_options.add_argument('--disable-save-password-bubble')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

user_agent = UserAgent()
chrome_options.add_argument(f"user-agent={user_agent.random}")

#driver = webdriver.Chrome(options=chrome_options)
#лшкфлшкф11
def login(driver):
    try:
        driver.get('https://www.blackhatlinks.com/members/login.php')
        driver.maximize_window()
        driver.execute_script("window.scrollBy(0, 100);")

        try:
            login_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="username"]'))
            )
            login_input.send_keys(user_login)
        except Exception as e:
            print(f"LOGIN INPUT ERROR \n{e}")

        try:
            pass_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]'))
            )
            pass_input.send_keys(user_password)
        except Exception as e:
            print(f"PASS INPUT ERROR \n{e}")

        log_in = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="frmSignIn"]/div[4]/div/input[3]'))
        )
        log_in.click()

        sleep(2)
    except Exception as e:
        print(f"LOGIN ERROR -- \n{e}")

def get_wallet_data():
    try:
        with webdriver.Chrome(options=chrome_options) as driver:
            login(driver)
            driver.get('https://www.blackhatlinks.com/members/bitcoin_credits.php')

            driver.execute_script("window.scrollBy(0, 850);")

            try:
                pay_button = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="feature-list"]/div/section/div[2]/div/div[1]/div/ul/li[2]/input[1]'))
                )
                pay_button.click()
            except Exception as e:
                print(f"PAY WITH CRYPTO BUTTON ERROR -- \n{e}")

            try:
                select_trc20 = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/bp-app/div/bp-public-invoice-view/div/div/div/div/bp-public-invoice-card/div/div/div/bp-public-invoice-card-state-prepared/div/div/bp-public-invoice-price-button[4]/div/div/button/span'))
                )
                select_trc20.click()

                tron_click = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/bp-app/div/bp-public-invoice-view/div/div/div/div/bp-public-invoice-card/div/div/div/bp-public-invoice-card-state-prepared/div/div/bp-public-invoice-price-button/div/div/button/span'))
                )
                tron_click.click()
            except Exception as e:
                print(f"SELECT TRC20 ERROR \n{e}")

            amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '/html/body/bp-app/div/bp-public-invoice-view/div/div/div/div/bp-public-invoice-card/div/div/div/bp-public-invoice-card-state-active/bp-public-invoice-qr-code/div/p[2]'))
            )
            amount = amount.text.replace("USDT", "")
    #<span id="black-tooltip" class="public-invoice-black-tooltip in-active-state">TCiC6KwkpYwFHmSKctcKFh8C6Gr5judjii</span>

            actions = ActionChains(driver)
            try:
                address = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '/html/body/bp-app/div/bp-public-invoice-view/div/div/div/div/bp-public-invoice-card/div/div/div/bp-public-invoice-card-state-active/bp-public-invoice-qr-code/div/p[3]/span[2]/span/span[1]'))
                )
                actions.move_to_element(address).perform()
            except Exception as e:
                print(f"ADDRESS ERROR \n{e}")
            try:
                address_res = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'black-tooltip'))
                )
                address_res = address_res.text
            except Exception as e:
                print(f"ADRESS RES ERROR \n{e}")

            return {
                "address": address_res,
                "amount": amount,
                "currency": "usdt"
            }
    except Exception as e:
        print(f"GET WALLET ERROR \n{e}")
        return None

@app.route('/api/selenium/blackhatlinks')
def wallet():
    wallet_data = get_wallet_data()
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5018)