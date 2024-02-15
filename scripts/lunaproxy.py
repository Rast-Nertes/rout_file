import cloudscraper
import requests
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

#Paymentmars

#CONSTANS
app = Flask(__name__)
scrap = cloudscraper.create_scraper()
user_login = 'kiracase34@gmail.com'
user_password = 'kiramira34'
url = 'https://www.lunaproxy.com/login/'

#API CONSTANS
api_key = '7f728c25edca4f4d0e14512d756d6868'

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

#driver = webdriver.Chrome(options=options)

def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        input_email = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="loginbox"]/div/div/div[3]/input'))
        )
        input_email.send_keys(user_login)

        input_password = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="loginbox"]/div/div/div[4]/input'))
        )
        input_password.send_keys(user_password)

        try:
            continue_log_in = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="loginbox"]/div/div/div[6]'))
            )
            continue_log_in.click()
            #Время, чтобы залогинился
            sleep(5)
        except Exception as e:
            print(f"LOG IN BUTTON ERROR \n{e}")

    except Exception as e:
        print(f"INPUT ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        driver.get("https://www.lunaproxy.com/buy-proxy/")
        driver.execute_script("window.scrollBy(0, 100);")

        try:
            choose_tariff = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[1]/div[6]/div[1]/div[1]/div[7]'))
            )
            choose_tariff.click()
        except Exception as e:
            print(f"CHOOSE TARIFF ERROR \n{e}")

        try:
            choose_crypto = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[7]/div[1]/div/div[3]'))
            )
            choose_crypto.click()
            sleep(2)

        except Exception as e:
            print(f"CHOOSE CRYPTO ERROR \n{e}")

        try:
            continue_to_pay = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[4]/div[1]'))
            )
            continue_to_pay.click()
        except Exception as e:
            print(f"CONTINUE ERROR \n{e}")

        try:
            choose_usdt = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[1]/div[7]/div[6]/div[2]'))
            )
            choose_usdt.click()
        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")

        try:
            continue_to_pay_2 = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[1]/div[1]'))
            )
            continue_to_pay_2.click()
        except Exception as e:
            print(f"CONTINUE_2 ERROR \n{e}")

        sleep(5)
        new_window = driver.window_handles[1]
        driver.switch_to.window(new_window)

        trc_20 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[1]/div[2]/div/div[1]')
        driver.execute_script("arguments[0].click();", trc_20)

        driver.execute_script("window.scrollBy(0, 300);")

        amount = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[1]/div[3]/div[7]/div[2]/div[1]/p/i'))
        )
        amount = amount.text.replace("USDT", "")

        address = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[1]/div[3]/div[7]/div[1]/div[1]/p'))
        )
        address = address.text

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }

@app.route('/api/selenium/lunaproxy')
def wallet():
    wallet_data = get_wallet()
    #print(wallet_data)
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5031)