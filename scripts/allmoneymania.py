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

url = 'https://allmoneymania.com/?a=login'
user_email = "alex37347818"
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
        input_email = driver.find_element(By.CSS_SELECTOR, 'body > section.bannera.position-relative.py-4 > div > div > div > div > form > div.row > div > div:nth-child(1) > input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'body > section.bannera.position-relative.py-4 > div > div > div > div > form > div.row > div > div:nth-child(2) > input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'body > section.bannera.position-relative.py-4 > div > div > div > div > form > div:nth-child(8) > div > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)

        sleep(3)
        driver.get('https://allmoneymania.com/?a=deposit')
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.CSS_SELECTOR, 'div.table-responsive.trans-table > table > tbody > tr:nth-child(10) > td:nth-child(2) > input[type=radio]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(10)
            submit = driver.find_element(By.CSS_SELECTOR, 'div.main-content.container-fluid > div:nth-child(3) > div > div > div.make-btn.text-center > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit)
        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(40)
            address = driver.find_element(By.CSS_SELECTOR, '#usdt\.trc20_form > i > a').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, 'div > div.table-responsive.trans-table > table > tbody > tr:nth-child(8) > td:nth-child(2)').text

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
