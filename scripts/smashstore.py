import requests
from seleniumwire import webdriver
from time import sleep
from flask import Flask, jsonify
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

#Zerocryptopay

#CONSTANS

app = Flask(__name__)
url = 'https://smashstore.me/en'
user_login = 'kiracase34@gmail.com'
user_password = 'oleg123567'

#API CONSTANS

API_KEY = '7f728c25edca4f4d0e14512d756d6868'
API_URL = 'http://rucaptcha.com/in.php'
API_RESULT_URL = f'http://rucaptcha.com/res.php?key={API_KEY}&action=get'

#CHROME OPTIONS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.headless = False
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

#driver = webdriver.Chrome(options=options)

def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        driver.maximize_window()
        try:
            driver.implicitly_wait(10)
            buy_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[23]/td[4]/a')
            driver.execute_script("arguments[0].click();", buy_button)
        except Exception as e:
            print(f"BUY BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            count = driver.find_element(By.XPATH, '//*[@id="end-number"]')
            driver.execute_script("arguments[0].click();", count)

            driver.implicitly_wait(10)
            input_email = driver.find_element(By.XPATH, '//*[@id="row-box-email"]')
            input_email.clear()
            input_email.send_keys(user_login)

            driver.implicitly_wait(10)
            input_count = driver.find_element(By.XPATH, '//*[@id="end-number"]')
            input_count.clear()
            input_count.send_keys('1')
        except Exception as e:
            print(f"INPUT ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_crypto_pay = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/button[2]')
            driver.execute_script("arguments[0].click();", choose_crypto_pay)
        except Exception as e:
            print(f"CHOOSE CRYPTO BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_tether = driver.find_element(By.XPATH, '//*[@id="form-send-money"]/div[1]/div/div/div')
            driver.execute_script("arguments[0].click();", choose_tether)

            driver.implicitly_wait(10)
            continue_button = driver.find_element(By.XPATH, '//*[@id="form-send-money"]/div[3]/button')
            driver.execute_script("arguments[0].click();", continue_button)
        except Exception as e:
            print(f"CHOOSE TETHER BUTTON ERROR \n{e}")

        amount = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="sum_p"]'))
        )
        amount = amount.get_attribute("value")

        address = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="youSend"]'))
        )
        address = address.get_attribute("value")

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }

def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
