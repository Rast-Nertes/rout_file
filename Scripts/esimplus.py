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
                button_buy = driver.find_element(By.XPATH, '/html/body/div[6]/div/div[2]/div[2]/button[3]').click()
            except Exception as e:
                pass

            driver.execute_script("window.scrollBy(0, 550);")
            try:
                choose_one_month = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/div[6]/label[1]'))
                )
                driver.execute_script("arguments[0].click();", choose_one_month)

                get_num = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/div/div[2]/button'))
                )
                driver.execute_script("arguments[0].click();", get_num)
            except Exception as e:
                print(f"CHOOSE ERROR \n{e}")

            try:
                cryptocurrency = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/button[3]'))
                )
                cryptocurrency.click()

                trc_20_choose = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div/div[1]/div/div[1]/div/div[2]/form/div[2]/ul/li[1]'))
                )
                trc_20_choose.click()

                next_step = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="btn-sub"]'))
                )
                next_step.click()
            except Exception as e:
                print(f"CRYPTO ERROR \n{e}")

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
        print(f"GET WALLET ERROR \n{e}")
        return None

@app.route('/api/selenium/esimplus')
def wallet():
    wallet_data = get_wallet()
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5022)
