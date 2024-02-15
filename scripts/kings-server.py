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
#import config
from time import sleep
import json

#driver = webdriver.Chrome()
app = Flask(__name__)

API_KEY = "7f728c25edca4f4d0e14512d756d6868" # ruCaptcha api-key
USERNAME = "kiracase34@gmail.com" # username
PASSWORD = "kiramiraoleg11" # password

def solve_captcha(sitekey: str, url: str) -> str:
    solver = TwoCaptcha(API_KEY)
    result = solver.recaptcha(sitekey=sitekey, url=url, invisible=1)
    return result["code"]

def captcha_and_login(driver):
    url = "https://control.king-servers.com/index.php?rp=/login"
    driver.maximize_window()
    driver.get(url); driver.implicitly_wait(60)
    captcha_code = solve_captcha('6LfexiYkAAAAAD-V3twFrBXyokmmVESnWLonrJo7', url)
    driver.execute_script(f'var textarea = document.getElementById("g-recaptcha-response"); textarea.style.display = "block"; textarea.innerHTML = "{captcha_code}";')
    driver.find_element(By.NAME, "username").send_keys(USERNAME); sleep(2)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD, Keys.ENTER); sleep(2)

def get_wallet():
    with webdriver.Chrome() as driver:
        actions = ActionChains(driver)
        captcha_and_login(driver)

        billing_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="menu"]/li[2]/a'))
        )
        billing_button.click()

        try:
            add_funds = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'Primary_Navbar-Billing-Add_Funds'))
            )
            add_funds.click()

            choose_payment_method = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="main-body"]/div/div/div[2]/div/div/div/div[1]/form/div/div[2]/div[2]/div[7]/label'))
            )
            choose_payment_method.click()
        except Exception as e:
            print(f"ADD FUNDS ERROR \n{e}")

        try:
            make_payment = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="main-body"]/div/div/div[2]/div/div/div/div[1]/form/div/div[3]/button'))
            )
            make_payment.click()

            sheepy_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]'))
            )
            sheepy_button.click()
        except Exception as e:
            print(f"MAKE PAYMENT ERROR \n{e}")

        try:
            choose_TRC20 = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/article/div/section/div[1]'))
            )
            choose_TRC20.click()

            actions.send_keys(Keys.ARROW_UP).perform()
            sleep(1)
            actions.send_keys(Keys.ARROW_UP).perform()
            sleep(1)
            actions.send_keys(Keys.ARROW_UP).perform()
            sleep(1)
            actions.send_keys(Keys.ENTER).perform()
            sleep(1)

            button_to_payment_details = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/article/div/section/button'))
            )
            button_to_payment_details.click()
            sleep(2)
        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")

        driver.execute_script("window.scrollBy(0, 300);")

        address = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/article/div/div/div[3]/div[2]/div/span'))
        )
        address = address.text

        amount = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/article/div/div/div[3]/div[1]/div/span'))
        )
        amount = amount.text.replace("USDT", "")

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }

@app.route('/api/selenium/king-servers')
def wallet():
    wallet_data = get_wallet()
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5031)