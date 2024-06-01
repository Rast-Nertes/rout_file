import time

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


def get_wallet():
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get('https://esimplus.me/virtual-phone-number/united-states/alabama?phone=%2B16197989936')
        driver.maximize_window()

        try:
            driver.implicitly_wait(10)
            get_num = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/button')
            driver.execute_script("arguments[0].click();", get_num)
        except Exception as e:
            return {"status":"0", "ext":f"error accept button {e}"}

        try:
            driver.implicitly_wait(10)
            choose_crypto_currency = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[1]/button[3]')
            driver.execute_script("arguments[0].click();", choose_crypto_currency)
        except Exception as e:
            return {"status":"0", "ext":f"error choose cryptocurrency {e}"}

        try:
            driver.implicitly_wait(10)
            choose_tether_trc20 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div[1]/div/div[1]/div/div[2]/form/div[2]/ul/li[1]')
            driver.execute_script("arguments[0].click();", choose_tether_trc20)

            driver.implicitly_wait(10)
            next_step_button = driver.find_element(By.CSS_SELECTOR, '#btn-sub')
            driver.execute_script("arguments[0].click();", next_step_button)
        except Exception as e:
            return {"status":"0", "ext":f"error choose trc20 {e}"}

        try:
            time.sleep(5)
            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH,'(//div[@class="pay-currency-addres__hesh"])[1]')
            amount = amount_elem.text.replace(' USDT TRC20', '')

            driver.implicitly_wait(20)
            address_elem = driver.find_element(By.XPATH, '(//a[@target="_blank"])[1]')
            address = address_elem.get_attribute('href').split("address/")[1]

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
