import requests
from selenium import webdriver
from time import sleep
from flask import Flask, jsonify
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Zerocryptopay

#CONSTANS
app = Flask(__name__)
user_login = 'kiracase34@gmail.com'
user_password = 'GGGggg1212'
url = 'https://farmfb.store'

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

        driver.execute_script("window.scrollBy(0, 550);")

        try:
            buy = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/section/table/tbody/tr[2]/td[4]/div/button'))
            )
            buy.click()

            buy_step2 = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/section/table/tbody/tr[2]/td[4]/div/ul/li[1]/a'))
            )
            buy_step2.click()
        except Exception as e:
            print(f"Wallet choose \n{e}")

        try:
            counts_product = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="end-number"]'))
            )
            counts_product.clear()
            counts_product.send_keys("2")

            input_email = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="row-box-email"]'))
            )
            input_email.send_keys(user_login)

        except Exception as e:
            print(f"INPUT PRODUCTS INFORM\n{e}")

        try:
            ticket = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="setpaidway"]/div/div/div[2]/div[2]/input'))
            )
            ticket.click()
            sleep(2)
            driver.execute_script("window.scrollBy(0, 400);")

            choose_zerocryptopay = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/div/div[3]/div/div/div[2]/div[3]/button[9]'))
            )
            choose_zerocryptopay.click()

            sleep(1)
            driver.execute_script("window.scrollBy(0, 500);")
            sleep(1)
        except Exception as e:
            print(f"CRYPTO CHOOSE ERROR \n{e}")

        try:
            choose_usdt_trc20 = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="form-send-money"]/div[1]/div/div[5]/div'))
            )
            choose_usdt_trc20.click()

            step_to_pay = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="form-send-money"]/div[3]/button'))
            )
            step_to_pay.click()

        except Exception as e:
            print(f"CHOOSE USDT ERROR \n{e}")

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

@app.route("/api/selenium/farmfb")
def wallet():
    wallet_data = get_wallet()
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5028)