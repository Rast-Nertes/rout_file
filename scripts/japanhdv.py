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

url = 'https://join.japanhdv.com/signup/signup.php'
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
        input_data(driver, 45, '//*[@id="email"]', user_email)
    except Exception as e:
        print(f'ERROR INPUT EMAIL \n{e}')

    try:
        click(driver, 35, '//*[@id="form"]/label[3]')
    except Exception as e:
        print(f'ERROR CHOOSE CRYPTO \n{e}')

    try:
        click(driver, 20, '//*[@id="join_normal_crypto"]/label[1]')
        sleep(1)
        click(driver, 20, '//*[@id="form"]/input[22]')
    except Exception as e:
        print(f"ERROR SUBMIT BUTTON \n{e}")

    try:
        input_data(driver, 45, '//*[@id="first_name"]', "Kira")
        sleep(1)
        input_data(driver, 20, '//*[@id="last_name"]', 'Ivanova')
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    try:
        click(driver, 45, '//*[@id="btn_USDT.TRC20"]')
        sleep(1)
        input_data(driver, 20, '//*[@id="bstable"]/tbody/tr[11]/td/input', user_email)
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    try:
        click(driver, 20, '//*[@id="btnCheckout"]')
    except Exception as e:
        print(f'ERROR SUBMIT \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(4.5)
            driver.implicitly_wait(40)
            amount = driver.find_element(By.XPATH, '//*[@id="helpa1"]/strong[1]').text.replace("USDT.TRC20", '').replace(" ", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="helpa1"]/strong[2]').text

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
