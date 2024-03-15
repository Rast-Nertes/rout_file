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

url = 'https://conspro.biz'
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
        input_email = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td:nth-child(1) > form > table > tbody > tr:nth-child(3) > td:nth-child(2) > input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td:nth-child(1) > form > table > tbody > tr:nth-child(4) > td:nth-child(2) > input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td > table > tbody > tr > td:nth-child(1) > form > table > tbody > tr:nth-child(5) > td:nth-child(2) > input')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")
    sleep(3)
    driver.get('https://conspro.biz/?a=deposit')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        try:
            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td.bgcolormain > table > tbody > tr > td > div > form > table:nth-child(10) > tbody > tr:nth-child(4) > td:nth-child(2) > input[type=radio]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(10)
            spend_button = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td.bgcolormain > table > tbody > tr > td > div > form > table:nth-child(12) > tbody > tr:nth-child(3) > td > input')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", spend_button)
        except Exception as e:
            print(f'CHOOSE TRC20 ERROR \n{e}')

        try:
            driver.implicitly_wait(40)
            address = driver.find_element(By.CSS_SELECTOR, '#coinpr_form > i > a').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td > table > tbody > tr > td.bgcolormain > table > tbody > tr > td > div > table > tbody > tr:nth-child(8) > td').text

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
