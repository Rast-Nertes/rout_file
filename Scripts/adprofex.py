from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from flask import Flask, jsonify
from twocaptcha import TwoCaptcha
from selenium import webdriver
from time import sleep

#driver = webdriver.Chrome()
app = Flask(__name__)

API_KEY = "7f728c25edca4f4d0e14512d756d6868" # ruCaptcha api-key
USERNAME = "kiracase34@gmail.com" # username
PASSWORD = "kiraadpro9" # password

def solve_captcha(sitekey: str, url: str) -> str:
    solver = TwoCaptcha(API_KEY)
    result = solver.recaptcha(sitekey=sitekey, url=url, invisible=1)
    return result["code"]

def captcha_and_login(driver):
    url = "https://advertiser.adprofex.com/login"
    driver.maximize_window()
    driver.get(url); driver.implicitly_wait(30)
    captcha_code = solve_captcha('6LcbPqMmAAAAAIIZTlt7AwAmV4z32HIst1aix5Gr', url)
    print(captcha_code)
    driver.execute_script(f'var textarea = document.getElementById("g-recaptcha-response-100000"); textarea.style.display = "block"; textarea.innerHTML = "{captcha_code}";')
    try:
        input_email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div/form/div[1]/div[1]/label/div/div[1]/div/input'))
        )
        input_email.send_keys(USERNAME)

        input_password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div/form/div[1]/div[2]/label/div/div[1]/div[1]/input'))
        )
        input_password.send_keys(PASSWORD)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        click_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="q-app"]/div/div[2]/div[2]/div/div/form/div[2]/div/button'))
        )
        click_button.click()
    except Exception as e:
        print(f"CLICK ERROR \n{e}")

def get_wallet():
    with webdriver.Chrome() as driver:
        captcha_and_login(driver)
        sleep(5)
        driver.get('https://advertiser.adprofex.com/lk/balance')

        try:
            add_funds = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="q-app"]/div/div[3]/main/div/div/div/div[2]/button'))
            )
            add_funds.click()

            choose_wallet = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="q-app"]/div/div[3]/main/div/div/div/div[2]/div[1]/div/div/div[6]/div[2]/div[2]'))
            )
            choose_wallet.click()

        except Exception as e:
            print(f"ADD FUNDS ERROR \n{e}")

        try:
            choose_capitalist_method = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="q-app"]/div/div[3]/main/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]'))
            )
            choose_capitalist_method.click()
        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")

        try:
            ticket = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="q-app"]/div/div[3]/main/div/div/div/div[2]/div[3]/label/div'))
            )
            ticket.click()

            add_funds_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="q-app"]/div/div[3]/main/div/div/div/div[2]/div[4]/button[2]'))
            )
            add_funds_button.click()
        except Exception as e:
            print(f"TICKET CHOOSE ERROR \n{e}")

        address = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="order-page"]/div[4]/div/div/div[3]/div[2]/div[2]/div[2]/button/span'))
        )
        address = address.text

        amount = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="order-page"]/div[4]/div/div/div[4]/div/div/div[3]/div[2]/strong'))
        )
        amount = amount.text

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }

def wallet():
    wallet_data = get_wallet()
    return wallet_data

if __name__ == "__main__":
    wallet()
