from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://secure.squirtingvirgin.com/signup/signup.php?'
user_name = "Spongegege12"
user_email = "leonidstakanov11@gmail.com"
user_password = "Qwerty62982"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1)
    driver.execute_script("arguments[0].click();", elem_click)
    sleep(1)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        input_data(driver, 35, '//*[@id="email"]', user_email)
        sleep(1)
        input_data(driver, 35, '//*[@id="password"]', user_password)
    except Exception as e:
        print(f"ERROR INPUT DATA \n{e}")

    try:
        click(driver, 20, '//*[@id="crypto-cascade"]')
        sleep(1)
        click(driver, 10, '//*[@id="submit-button"]')
    except Exception as e:
        print(f"ERROR CHOOSE CRYPTO \n{e}")

    try:
        click(driver, 35, '/html/body/div[2]/div[3]/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div/button')
    except Exception as e:
        print(f'ERROR CHOOSE CRYPTO METHOD \n{e}')

    try:
        click(driver, 30, '//*[@id="root"]/div[1]/div/div[3]/div[2]/div/div[10]')
    except Exception as e:
        print(f"ERROR CHOOSE TRC20 \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(5)
            driver.implicitly_wait(40)
            amount = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[3]').text

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div[1]').text

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
