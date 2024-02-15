import requests
from PIL import Image
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
user_password = 'oleg123123'

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
            driver.get('https://esimplus.me/virtual-phone-number/united-states/alabama?phone=%2B16197989936')
            driver.maximize_window()

            try:
                driver.implicitly_wait(10)
                choose_month_tariff = driver.find_element(By.CSS_SELECTOR, 'div.sc-1cb45200-14.gShvJM > div.sc-1cb45200-15.ifOnEc > label:nth-child(1)')
                driver.execute_script("arguments[0].click();", choose_month_tariff)

                driver.implicitly_wait(10)
                get_num = driver.find_element(By.CSS_SELECTOR, 'div.sc-7a9d20cb-3.sc-ef50f70f-0.WBcIA.fkgzzt > div > div.sc-1cb45200-14.gShvJM > button')
                driver.execute_script("arguments[0].click();", get_num)
            except Exception as e:
                print(f"CHOOSE MONTH TARIFF ERROR \n{e}")

            try:
                driver.implicitly_wait(10)
                choose_crypto_currency = driver.find_element(By.CSS_SELECTOR, 'div.sc-8f6f74e3-1.cwBvbl > button:nth-child(2)')
                driver.execute_script("arguments[0].click();", choose_crypto_currency)
            except Exception as e:
                print(f"CHOOSE CRYPTO CURRENCY ERROR \n{e}")

            try:
                driver.implicitly_wait(10)
                choose_tether_trc20 = driver.find_element(By.CSS_SELECTOR, 'div.search-currency > form > div.list-container > ul > li:nth-child(1)')
                driver.execute_script("arguments[0].click();", choose_tether_trc20)

                driver.implicitly_wait(10)
                next_step_button = driver.find_element(By.CSS_SELECTOR, '#btn-sub')
                driver.execute_script("arguments[0].click();", next_step_button)
            except Exception as e:
                print(f"CHOOSE TRC20 ERROR \n{e}")

            try:
                amount = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="app"]/div/div/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[3]/div[1]/div[2]'))
                )
                amount = amount.text.replace(' USDT TRC20', '')

                address = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//*[@id="app"]/div/div/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[3]/div[2]/div[2]'))
                )
                address = address.text

                return {
                    "address": address,
                    "amount": amount,
                    "currency": "usdt"
                }
            except Exception as e:
                print(f"DATA ERROR \n{e}")
                return None


    except Exception as e:
        print(f"GET WALLET ERROR \n{e}")
        return None

def wallet():
    wallet_data = get_wallet()
    return jsonify(wallet_data)

