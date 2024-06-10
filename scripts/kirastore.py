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

#Zerocryptopay

#CONSTANS

user_login = 'kiracase34@gmail.com'
#user_password = 'kiramira34'
url = 'https://kirastore.info'

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        driver.maximize_window()

        driver.execute_script("window.scrollBy(0, 200);")

        try:
            buy_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="fn_set_wraps"]/div[2]/main/div[4]/div[2]/div/div[2]/div/div[3]/button[1]'))
            )
            buy_button.click()
        except Exception as e:
            print(f"BUY BUTTON ERROR \n{e}")

        try:
            input_email = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="setpaidway"]/div[3]/form/div[2]/div[1]/input'))
            )
            input_email.send_keys(user_login)

            choose_zerocryptopay = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="setpaidway"]/div[3]/form/div[4]/label[2]'))
            )
            choose_zerocryptopay.click()

            try:
                buy = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="setpaidway"]/div[3]/form/div[6]/div[2]/button'))
                )
                driver.execute_script("arguments[0].click();", buy)
            except Exception as e:
                print(f"BUY ERROR \n{e}")
            sleep(1)
            driver.execute_script("window.scrollBy(0, 400);")
        except Exception as e:
            print(f"INPUT ERROR \n{e}")

        try:
            choose_usdt_trc20 = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="form-send-money"]/div[1]/div/div[2]/div'))
            )
            choose_usdt_trc20.click()

            step_to_pay = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="form-send-money"]/div[3]/button'))
            )
            driver.execute_script("arguments[0].click();", step_to_pay)

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
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
