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

#PAYEER

#CONSTANS

app = Flask(__name__)
url = 'https://www.coinsbee.com/ru/login'
user_login = 'kiramira123'
user_email = 'kiracase34@gmail.com'
user_password = 'KIRAKIRA123'

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

#PROXY_CONSTANS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@45.130.254.133:8000",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def login(driver):
    driver.get('https://justanotherpanel.com/?redirect=%2Faddfunds')
    driver.maximize_window()

    try:
        input_email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="username"]'))
        )
        input_email.send_keys(user_login)

        input_password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]'))
        )
        input_password.send_keys(user_password)
        sleep(2)

        log_in = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '(//input[@type="submit"])[1]'))
        )
        log_in.click()
    except Exception as e:
        return {"status": "0", "ext": f"error login {e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)
        driver.get('https://justanotherpanel.com/addfunds')

        try:
            specify_currency = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="amount"]'))
            )
            specify_currency.send_keys('10')

            pay_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '(//button[@type="submit"])[2]'))
            )
            pay_button.click()
        except Exception as e:
            return {"status": "0", "ext": f"error specify {e}"}

        try:
            usdt_ = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@class="ps_name" and text()="USDT"]'))
            )
            usdt_.click()

            input_email = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="id_order_email"]'))
            )
            input_email.send_keys(user_email)

            accept_wallet = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/form/div[2]/div[4]/div[2]/a'))
            )
            accept_wallet.click()
        except Exception as e:
            return {"status": "0", "ext": f"error usdt choose {e}"}

        sleep(5)

        try:
            amount = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="info_bitcoin"]/div[1]/h3/font[1]'))
            )
            amount = amount.text.replace("USDT", "")

            address = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="info_bitcoin"]/div[1]/h3/font[2]'))
            )
            address = address.text
            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            return {"status": "0", "ext": f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
