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

#Zerocryptopay

#CONSTANS
app = Flask(__name__)
scrap = cloudscraper.create_scraper()
user_login = 'kiracase34@gmail.com'
user_password = ''
url = 'https://smashstore.me/en'

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
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        driver.maximize_window()

        try:
            driver.implicitly_wait(10)
            click_buy_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr[9]/td[4]/a')
            driver.execute_script("arguments[0].click();", click_buy_button)
        except Exception as e:
            print(f"CLICK BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_count = driver.find_element(By.XPATH, '//*[@id="end-number"]')
            input_count.clear()
            input_count.send_keys("1")

            driver.implicitly_wait(10)
            input_email = driver.find_element(By.XPATH, '//*[@id="row-box-email"]')
            input_email.clear()
            input_email.send_keys(user_login)

        except Exception as e:
            print(f"INPUT ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            crypto_pay_button = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/button[2]')
            driver.execute_script("arguments[0].click();", crypto_pay_button)
        except Exception as e:
            print(f"CHOOSE CRYPTO ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            choose_wallet = driver.find_element(By.XPATH, '//*[@id="form-send-money"]/div[1]/div/div/div')
            driver.execute_script("arguments[0].click();", choose_wallet)

            driver.implicitly_wait(10)
            next_step = driver.find_element(By.XPATH, '//*[@id="form-send-money"]/div[3]/button')
            driver.execute_script("arguments[0].click();", next_step)
        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")

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
            address = address.get_attribute("value")

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")

def wallet():
    wallet_data = get_wallet()
    return wallet_data

if __name__ == "__main__":
    wallet()