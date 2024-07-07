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

url = 'https://trust-fx.com/?a=login'
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
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.CSS_SELECTOR, '#login-form > label:nth-child(7) > input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, '#login-form > label:nth-child(8) > input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, '#login-form > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)

        sleep(2.5)
        driver.get('https://trust-fx.com/?a=deposit')
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(10)
            send_button = driver.find_element(By.CSS_SELECTOR, 'section > div.content__inner > div.content__main.scroll > form > div.form > div > div.form__item.form__item--amount > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", send_button)
        except Exception as e:
            print(f"SEND BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//a[@class="wallet-address"]').get_attribute('href').split('tron:')[1]

            driver.implicitly_wait(10)
            amount = driver.find_element(By.XPATH, '//*[@id="usdt.trc20_form"]/b').text.replace("Tether TRC20", '').replace("USDT", "").replace(" ", '')

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
