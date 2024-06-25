from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://bitcashdeposit.com/?a=login'
user_email = "kiracase34"
user_password = "eE@j736wbLTWTd"

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
        input_email = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(1) > td:nth-child(2) > input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(2) > td:nth-child(2) > input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr:nth-child(3) > td:nth-child(2) > input')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")
    sleep(3)
    driver.get('https://bitcashdeposit.com/?a=deposit')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.CSS_SELECTOR, 'form > table:nth-child(27) > tbody > tr:nth-child(7) > td:nth-child(2) > input[type=radio]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(10)
            submit_button = driver.find_element(By.CSS_SELECTOR, 'form > table:nth-child(29) > tbody > tr:nth-child(3) > td > input')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit_button)
        except Exception as e:
            print(f"ERROR CHOOSE TRC20 \n{e}")

        try:
            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR, '#coinpr_form > i > a').text

            driver.implicitly_wait(10)
            amount = driver.find_element(By.CSS_SELECTOR, 'body > center > table > tbody > tr:nth-child(8) > td').text

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
