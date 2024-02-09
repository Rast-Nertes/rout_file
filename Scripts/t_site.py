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
url = 'https://lteboost.com'

#API CONSTANS
api_key = '7f728c25edca4f4d0e14512d756d6868'

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

driver = webdriver.Chrome(options= options)

def get_wallet():
    driver.get(url)
    driver.maximize_window()

    driver.get('https://lteboost.com/?cat_id=5253')

    try:
        driver.implicitly_wait(10)
        buy_button = driver.find_element(By.XPATH, '//*[@id="fn_home_content"]/div[2]/div[2]/div[4]/div/a[1]')
        driver.execute_script("arguments[0].click();", buy_button)
    except Exception as e:
        print(f"BUY BUTTON ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        input_count = driver.find_element(By.XPATH, '//*[@id="end-number"]')
        input_count.clear()
        input_count.send_keys('1')

        driver.implicitly_wait(10)
        input_email = driver.find_element(By.XPATH, '//*[@id="row-box-email"]')
        input_email.clear()
        input_email.send_keys(user_login)

    except Exception as e:
        print(f"ERROR INPUT \n{e}")

    try:
        driver.implicitly_wait(10)
        ticket = driver.find_element(By.XPATH, '//*[@id="body"]/div[4]/div/div[2]/input')
        driver.execute_script("arguments[0].click();", ticket)

        driver.implicitly_wait(10)
        ticket_2 = driver.find_element(By.XPATH, '//*[@id="body"]/div[4]/div/div[3]/input')
        driver.execute_script("arguments[0].click();", ticket_2)
    except Exception as e:
        print(f"TICKETS ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        choose_crypto_button = driver.find_element(By.XPATH, '//*[@id="body"]/div[4]/div/div[4]/button[7]')
        driver.execute_script("arguments[0].click();", choose_crypto_button)
    except Exception as e:
        print(f"CHOOSE CRYPTO ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        choose_usdt_trc20 = driver.find_element(By.XPATH, '//*[@id="form-send-money"]/div[1]/div/div[5]/div')
        driver.execute_script("arguments[0].click();", choose_usdt_trc20)

        driver.implicitly_wait(10)
        next_step = driver.find_element(By.XPATH, '//*[@id="form-send-money"]/div[3]/button')
        driver.execute_script("arguments[0].click();", next_step)
    except Exception as e:
        print(f"CHOOSE PAYMENT METHOD \n{e}")

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
        print(f"DATA ERROR \n{e}")
        return None

def wallet():
    wallet_data = get_wallet()
    return wallet_data

if __name__ == "__main__":
    wallet()