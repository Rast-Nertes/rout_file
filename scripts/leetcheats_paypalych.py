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

url = 'https://leet-cheats.ru/signin'
user_email = "kiracase34"
user_password = "wyD37QVnCRweg8h"

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
        input_email = driver.find_element(By.CSS_SELECTOR, 'div.container > div > div > div:nth-child(1) > div > form > div.input-group.mb-3 > input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'div.container > div > div > div:nth-child(1) > div > form > div.input-group.mb-4 > input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'div.container > div > div > div:nth-child(1) > div > form > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    sleep(2)
    driver.get('https://leet-cheats.ru/profile')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(10)
            append_amount = driver.find_element(By.CSS_SELECTOR, 'div > div.col-12.col-md > div > div.row.mt-3.mt-md-0 > div:nth-child(1) > button:nth-child(3)')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", append_amount)
        except Exception as e:
            print(f"APPEND AMOUNT \n{e}")

        try:
            driver.implicitly_wait(10)
            input_amount = driver.find_element(By.ID, 'fillup_balance__amount')
            input_amount.clear()
            input_amount.send_keys("200")
        except Exception as e:
            print(f"INPUT ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_paypalych = driver.find_element(By.CSS_SELECTOR, 'div > form > div.modal-body > div > div.col-12 > label')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_paypalych)

            driver.implicitly_wait(10)
            next_step = driver.find_element(By.XPATH, '//*[@id="balanceEditor"]/div/div/form/div[2]/button[1]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step)
        except Exception as e:
            print(f"ERROR CHOOSE PAYMENT \n{e}")

        try:
            driver.implicitly_wait(10)
            submit_payment = driver.find_element(By.CSS_SELECTOR, 'div:nth-child(3) > div > div.payment-form > div.payment-form__main > div.transition-all.duration-500.opacity-100 > div > div > form:nth-child(1) > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit_payment)
        except Exception as e:
            print(f"ERROR CHOOSE TRC20 \n{e}")

        try:
            driver.implicitly_wait(10)
            address = driver.find_element(By.ID, 'link').text

            driver.implicitly_wait(10)
            amount = driver.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div.text-center.text-gray-mid.font-medium.mb-4.max-w-xs.mx-auto > span').text.replace("USDT", '').replace(' ', '').replace(',', '.')

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
