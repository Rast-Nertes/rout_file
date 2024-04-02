from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://miningfarm.store/login'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(50)
        input_email = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/form/div/table/tbody/tr[1]/td/input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(30)
        input_password = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/form/div/table/tbody/tr[2]/td/input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/form/div/table/tbody/tr[3]/td/input')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    sleep(3.5)
    driver.get('https://miningfarm.store/account/insert')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(30)
            choose_frekassa = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[5]/div/div/b/div[3]/div[3]/a/img')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_frekassa)

            driver.implicitly_wait(40)
            input_amoun = driver.find_element(By.XPATH, '//*[@id="oa"]')
            input_amoun.clear()
            input_amoun.send_keys("650")

            driver.implicitly_wait(30)
            submit = driver.find_element(By.ID, 'submit')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit)
        except Exception as e:
            print(f"ERROR CHOOSE FREEKASSA \n{e}")

        try:
            driver.implicitly_wait(30)
            next_step_button_2 = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[5]/div/div/div[2]/center/b/b/center/form/input[8]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step_button_2)
        except Exception as e:
            print(f'ERROR NEXT STEP BUTTON \n{e}')

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
