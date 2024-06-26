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

url = 'https://erobits.com/login/'
user_email = "rwork875@gmail.com"
user_password = "n7zg4z"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    driver.execute_script("arguments[0].click();", elem_click)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        input_data(driver, 20, '//*[@id="input-email"]', user_email)
        sleep(1)
        input_data(driver, 20, '//*[@id="input-password"]', user_password)
        sleep(1)
        click(driver, 20, '//*[@id="content"]/div/div[2]/div/form/input')
        sleep(3.5)
    except Exception as e:
        print(f'ERROR LOGN \n{e}')

    driver.get('https://erobits.com/futanari/futa-on-girl/the-visitor.html')

    try:
        click(driver, 20, '//*[@id="button-cart"]')
        sleep(1)
        click(driver, 20, '//*[@id="smpcpp-modal-footer"]/input[2]')
    except Exception as e:
        print(f'ERROR CHECKOUT \n{e}')

    try:
        click(driver, 20, '//*[@id="plisio"]')
        sleep(1)
        click(driver, 20, '//*[@id="buttons"]/div[1]/input')
    except Exception as e:
        print(f'ERROR CHOOSE WAL \n{e}')

    try:
        click(driver, 40, '/html/body/div/div/div[2]/div[2]/div/div[3]/div[13]/button/div')
        sleep(1)
        click(driver, 20, '/html/body/div/div/div[2]/div[2]/div/div[3]/div[2]/button/div')
    except Exception as e:
        print(f'ERROR TRC20 \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[7]').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '//*[@id="step_pay__amount_payTo"]').text

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
