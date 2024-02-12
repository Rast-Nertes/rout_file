from time import sleep
from flask import Flask
from flask import jsonify
#from selenium import webdriver
from fake_useragent import UserAgent
from seleniumwire import webdriver
#import undetected_chromedriver2 as uc2
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#CONSTANS

app = Flask(__name__)
url = 'https://ororo.tv/ru/shows'
user_login = 'kiracase34@gmail.com'
user_password = 'kiraoleg6'

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
        print("LOGIN START")
        driver.get(url)
        driver.maximize_window()

        button_to_login = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/div[1]/header/div/div/nav/div[3]/ul/li[1]/a'))
        )
        button_to_login.click()

        element_start__input_user_login = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="user_email"]'))
        )
        element_start__input_user_login.send_keys(user_login)

        #Вводим пароль

        input_user_password = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="user_password"]'))
        )
        input_user_password.send_keys(user_password)

        log_in = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="new_user"]/input[3]'))
        )
        log_in.click()

        sleep(5)
        print("LOGIN ACCEPT")
    except Exception as e:
        print(f"LOGIN ERROR -- \n{e}")

def get_wallet_data():
    try:
        with webdriver.Chrome(options=chrome_options) as driver:
            login(driver)
            driver.get('https://ororo.tv/ru/users/subscription')

            crypto_choose = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="payment-form"]/div[2]/div[2]/ul/li[2]/button'))
            )
            crypto_choose.click()

            driver.execute_script("window.scrollTo(0, 800);")

            usdt_choose = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[3]/div[15]/button'))
            )
            usdt_choose.click()

            usdt_20_choose = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[3]/div[2]/button'))
            )
            usdt_20_choose.click()

            amount = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="step_pay__amount_payTo"]'))
            )
            amount = amount.text

            address = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[7]'))
            )
            address = address.text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
    except Exception as e:
        print(f"GET WALLET ERROR -- \n{e}")
        return None

@app.route('/api/selenium/ororo')
def wallet():
    wallet_data = get_wallet_data()
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5015)