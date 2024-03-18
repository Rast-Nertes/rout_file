from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://cryptorhino.limited/login'
user_email = "alex37347818@gmail.com"
user_password = "Pq9aiYkiFN6iR6N"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.ID, 'username')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.ID, 'passcode')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, '#loginForm > div:nth-child(4) > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    sleep(2)
    driver.get('https://cryptorhino.limited/deposit')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(10)
            choose_wallet = driver.find_element(By.CSS_SELECTOR, '#dpm-list > li > label')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_wallet)

            driver.implicitly_wait(10)
            deposit_now_button = driver.find_element(By.CSS_SELECTOR, '#pay-now')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", deposit_now_button)
        except Exception as e:
            print(f"ERROR CHOOSE WALLET \n{e}")

        try:
            driver.implicitly_wait(10)
            input_amount = driver.find_element(By.ID, 'prm-amnt')
            input_amount.clear()
            input_amount.send_keys("10")

            driver.implicitly_wait(5)
            continue_deposit = driver.find_element(By.ID, 'pay-next')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_deposit)

            driver.implicitly_wait(10)
            confirm_pay = driver.find_element(By.ID, 'pay-confirm')
            sleep(1.5)
            driver.execute_script("arguments[0].click(0);", confirm_pay)
        except Exception as e:
            print(f"ERROR CONTINUE DEPOSIT \n{e}")

        try:
            driver.implicitly_wait(20)
            address = driver.find_element(By.ID, 'wallet-address').get_attribute("value")

            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, 'div > div > div > div.nk-pps-card.card.card-bordered.popup-inside > div > div:nth-child(2) > div.pay-info.text-center > p').text.replace("USD", "").replace(" ", "")

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
