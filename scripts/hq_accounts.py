import cloudscraper
from selenium import webdriver
from time import sleep
from twocaptcha import TwoCaptcha
from flask import Flask, jsonify
from fake_useragent import UserAgent
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#ZeroCryptopay

#CONSTANS
app = Flask(__name__)
scrap = cloudscraper.create_scraper()
user_login = 'kiracase34@gmail.com'
#user_password = 'kiramira123!'
url = 'https://hq-accounts.com'

#API CONSTANS
api_key = '7f728c25edca4f4d0e14512d756d6868'

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

#driver = webdriver.Chrome(options= options)

def get_wallet():
    with webdriver.Chrome(options) as driver:
        driver.get('https://hq-accounts.com/category/facebook/fb-accounts-email-cookie-empty-ukraine.2009068?buygood=1')
        driver.maximize_window()

        try:
            choose_wallet = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/main/div/div/div/div[1]/div[1]/div[1]'))
            )
            choose_wallet.click()
        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")
            return None

        try:
            input_count = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/main/div/div/div/div[3]/div[1]/div[3]/input'))
            )
            input_count.clear()
            input_count.send_keys('1')

            input_email = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/main/div/div/div/div[3]/div[1]/div[4]/input'))
            )
            input_email.send_keys(user_login)
        except Exception as e:
            print(f"INPUT ERROR \n{e}")
            return None

        try:
            driver.implicitly_wait(10)
            ticket = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/div/div[3]/div[1]/div[6]/input')
            driver.execute_script("arguments[0].click();", ticket)

            buy = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="pay"]/input'))
            )
            buy.click()
        except Exception as e:
            print(f'BUY ERROR \n{e}')
            return None

        try:
            driver.implicitly_wait(10)
            choose_udst_trc20 = driver.find_element(By.XPATH, '//*[@id="form-send-money"]/div[1]/div/div[6]/div')
            driver.execute_script("arguments[0].click();", choose_udst_trc20)

            driver.implicitly_wait(10)
            accept_choose = driver.find_element(By.XPATH, '//*[@id="form-send-money"]/div[3]/button')
            driver.execute_script("arguments[0].click();", accept_choose)
        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")
            return None

        try:
            amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="sum_p"]'))
            )
            amount = amount.get_attribute('value')

            address = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="youSend"]'))
            )
            address = address.get_attribute('value')

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"INFO ERROR \n{e}")
            return None

def wallet():
    wallet_data = get_wallet()
    #print(wallet_data)
    return jsonify(wallet_data)
