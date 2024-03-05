from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://bestedplg.com/karton-cc-cvv-usa/'
user_login = "kiracase34"
user_password = "@@ED2BqKyJCW6@2"

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        driver.maximize_window()
        driver.get(url)

        try:
            driver.implicitly_wait(20)
            add_to_cart = driver.find_element(By.CSS_SELECTOR, 'div.summary.entry-summary > form > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", add_to_cart)
        except Exception as e:
            print(f"ADD TO CART BUTTON ERROR \n{e}")

        sleep(3)
        driver.get('https://bestedplg.com/checkout/')
        sleep(3)

        try:
            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.ID, 'headingTwo')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            address = driver.find_element(By.ID, 'usdtadr').get_attribute('value')

            driver.implicitly_wait(20)
            amount = driver.find_element(By.ID, 'usdtquan').get_attribute('value')

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
