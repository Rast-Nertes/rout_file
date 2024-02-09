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

url = 'https://my.unitalk.cloud/enter.html#auth'
API_KEY = "7f728c25edca4f4d0e14512d756d6868" # ruCaptcha api-key
USERNAME = "kiracase34@gmail.com" # username
PASSWORD = "0WvpZNBM" # password

def solve_captcha(sitekey: str, url: str) -> str:
    solver = TwoCaptcha(API_KEY)
    result = solver.recaptcha(sitekey=sitekey, url=url, invisible=1)
    return result["code"]

def captcha_and_login(driver):
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(60)
    captcha_code = solve_captcha('6LdTrQYeAAAAAB5wwjOovTVSrXDmPB7we-9dYi0o', url)
    #print(captcha_code)
    driver.execute_script(f'var textarea = document.getElementById("g-recaptcha-response-100000"); textarea.style.display = "block"; textarea.innerHTML = "{captcha_code}";')

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/input')
        input_email.send_keys(USERNAME)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/input')
        input_password.send_keys(PASSWORD)
    except Exception as e:
        print(f"ERROR INPUT \n{e}")

    try:
        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[6]/button')
        driver.execute_script("arguments[0].click();", login_button)
        sleep(5)
    except Exception as e:
        print(f"LOG IN BUTTON ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome() as driver:
        captcha_and_login(driver)
        driver.get('https://my.unitalk.cloud/index.html#balance')

        try:
            driver.implicitly_wait(10)
            input_amount = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[1]/div[2]/div[2]/div/div/label/input')
            input_amount.send_keys('5')

            driver.implicitly_wait(10)
            replenish = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[1]/div[2]/div[2]/div/button')
            driver.execute_script("arguments[0].click();", replenish)
        except Exception as e:
            print(f"REPLENISH ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_payment_method = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[3]/button')
            driver.execute_script("arguments[0].click();", choose_payment_method)

            # Animation
            sleep(2)
            driver.implicitly_wait(10)
            choose_crypto_payment_method = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[3]/ul/li[2]')
            driver.execute_script("arguments[0].click();", choose_crypto_payment_method)
        except Exception as e:
            print(f"CHOOSE PAYMENT ERROR \n{e}")

        try:
            #Animation
            sleep(2)
            driver.implicitly_wait(10)
            buy = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/button')
            driver.execute_script("arguments[0].click();", buy)
        except Exception as e:
            print(f"BUY ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_usdt_trc20 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div[1]/div/div[1]/div/div[2]/form/div[2]/ul/li[1]')
            driver.execute_script("arguments[0].click();", choose_usdt_trc20)

            driver.implicitly_wait(10)
            next_step = driver.find_element(By.XPATH, '//*[@id="btn-sub"]')
            driver.execute_script("arguments[0].click();", next_step)
        except Exception as e:
            print(f"ERROR CHOOSE \n{e}")

        amount = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[3]/div[1]/div[2]'))
        )
        amount = amount.text.replace('USDT TRC20 ', '')

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

def wallet():
    wallet_data = get_wallet()
    return wallet_data

if __name__ == "__main__":
    wallet()