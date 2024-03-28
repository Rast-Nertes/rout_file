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

url = 'https://pornoskazka9.org'
user_email = "kiracase34@gmail.com"
user_password = "Nd6WCNkv22FLXL3"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def login(driver):
    driver.get(url)
    driver.maximize_window()
    sleep(3.5)
    driver.refresh()
    try:
        driver.implicitly_wait(60)
        log_button = driver.find_element(By.XPATH, '//*[@id="mm-0"]/div[2]/div[2]/div[1]/div/div/div[1]/a')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", log_button)
    except Exception as e:
        print(f"ERROR LOG BUTTON \n{e}")

    try:
        driver.implicitly_wait(40)
        input_email = driver.find_element(By.XPATH, '//*[@id="login-form-rcl"]/form/div[1]/input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(30)
        input_password = driver.find_element(By.XPATH, '//*[@id="login-form-rcl"]/form/div[2]/input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '//*[@id="login-form-rcl"]/form/div[4]/a[1]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    sleep(3)
    driver.get('https://pornoskazka9.org/vip-dostup/')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(50)
            choose_tariff = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div/form/input[10]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_tariff)
        except Exception as e:
            print(f"ERROR CHOOSE TARIFF \n{e}")

        driver.refresh()
        sleep(3.5)

        try:
            driver.implicitly_wait(60)
            choose_trc20 = driver.find_element(By.ID, 'currency-15')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(40)
            input_email = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[1]/div/form/div/div[2]/input')
            input_email.clear()
            input_email.send_keys(user_email)
        except Exception as e:
            print(f"INPUT EMAIL \n{e}")

        try:
            driver.implicitly_wait(60)
            submit_payment = driver.find_element(By.ID, 'submit-payment')
            sleep(1.5)
            submit_payment.click()
        except Exception as e:
            print(f"SUBMIT ERROR \n{e}")

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[7]/div[2]').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[5]/span').text

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
