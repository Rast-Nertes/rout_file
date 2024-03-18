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

url = 'https://mixli.biz/?a=login'
user_email = "alex37347818"
user_password = "YRzVmP6b@HURzJ7"

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
        input_email = driver.find_element(By.CSS_SELECTOR, 'article > div.sign > div.sign__block > div.sign__content > form > div:nth-child(6) > input[type=text]')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'article > div.sign > div.sign__block > div.sign__content > form > div:nth-child(7) > input[type=password]')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'article > div.sign > div.sign__block > div.sign__content > form > div.sign__footer > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        sleep(2)

        driver.get('https://mixli.biz/?a=deposit')
        try:
            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.CSS_SELECTOR, 'div > form > div:nth-child(5) > div.profile-block__content > div > ul > li:nth-child(10) > label > span')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(10)
            input_amount = driver.find_element(By.CSS_SELECTOR, 'section:nth-child(3) > div > form > div:nth-child(6) > div.profile-block__content > div > div > input[type=text]')
            input_amount.clear()
            input_amount.send_keys('10')
        except Exception as e:
            print(f"INPUT TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            deposit_button = driver.find_element(By.CSS_SELECTOR, 'article > section:nth-child(3) > div > form > div:nth-child(6) > div.lk-buttons > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", deposit_button)
        except Exception as e:
            print(f"ERROR DEPOSIT BUTTON \n{e}")

        try:
            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR, '#usdt\.trc20_form > i > a').text.replace("(Token USDT)", '').replace(" ", "")

            driver.implicitly_wait(10)
            amount = driver.find_element(By.CSS_SELECTOR, '#usdt\.trc20_form > b').text.replace("USDT", "").replace(" ", '')

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
