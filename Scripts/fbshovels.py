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
url = 'https://fbshovels.com'

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
        driver.execute_script("window.scrollBy(0, 300);")
        try:
            button_buy = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/section/table/tbody/tr[3]/td[4]/div/button'))
            )
            button_buy.click()

            button_accept_buy = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/section/table/tbody/tr[3]/td[4]/div/ul/li[1]/a'))
            )
            button_accept_buy.click()
        except Exception as e:
            print(f"BUTTON BUY ERROR \n{e}")

        try:
            input_email = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="row-box-email"]'))
            )
            input_email.send_keys(user_login)

            input_count = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="end-number"]'))
            )
            input_count.clear()
            input_count.send_keys('1')

            choose_zerocrypto_pay = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="setEmailButton"]'))
            )
            choose_zerocrypto_pay.click()

        except Exception as e:
            print(f"ZEROCRYPTO ERROR \n{e}")

        try:
            choose_usdt_trc20 = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[2]/div/div/form/div[1]/div/div[2]/div'))
            )
            choose_usdt_trc20.click()

            driver.execute_script("window.scrollBy(0, 600);")
            sleep(2)
            step_to_pay = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="form-send-money"]/div[3]/button'))
            )
            step_to_pay.click()
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
            address = address.get_attribute('value')

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"INFO ERROR \n{e}")

@app.route("/api/selenium/fbshobels")
def wallet():
    wallet_data = get_wallet()
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5029)