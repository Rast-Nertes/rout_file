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

url = 'https://www.dividendgrowth.online'
user_email = "alex37347818"
user_password = "fHh@8DJgHbDps6U"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(20)
        button_to_login = driver.find_element(By.CSS_SELECTOR, 'div > ul > li > a.js-cart-animate.btn.btn-small2.btn-border.c-primary2')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", button_to_login)
    except Exception as e:
        print(f"BUTTON TO LOGIN ERROR \n{e}")

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.CSS_SELECTOR, 'div > form > input.email.input-standard-grey')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'div > form > input.password.input-standard-grey')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'div > form > div.login-btn-wrap > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        sleep(2)

        driver.get('https://www.dividendgrowth.online/?a=deposit')

        try:
            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.CSS_SELECTOR, 'div > form > table:nth-child(10) > tbody > tr:nth-child(8) > td:nth-child(2) > input[type=radio]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(10)
            submit = driver.find_element(By.CSS_SELECTOR, 'form > table:nth-child(12) > tbody > tr:nth-child(3) > td > input')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit)
        except Exception as e:
            print(f"ERROR CHOOSE TRC20 \n{e}")

        try:
            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR, '#coinpr_form > i > a').text

            driver.implicitly_wait(10)
            amount = driver.find_element(By.CSS_SELECTOR, 'div > table > tbody > tr:nth-child(5) > td').text

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
