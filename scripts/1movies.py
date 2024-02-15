#import undetected_chromedriver
from time import sleep
from flask import Flask, jsonify
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
#ALFACOINS

#CONSTANS
app = Flask(__name__)
user_login = 'kiracase34@gmail.com'
user_password = 'kirakira34'
url = 'https://torguard.net/clientarea.php'

options = webdriver.ChromeOptions()
options.headless = False
#driver = webdriver.Chrome(options=options)

def login():
    with webdriver.Chrome(options = options) as driver:
        driver.get(
            'https://1movies.life/user/premiummembership?utm_source=1movies&utm_medium=red_button&utm_campaign=premium&utm_content=guest')
        driver.maximize_window()
        try:
            continue_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="premium-data-trigger"]/div[3]/div[2]/div[3]'))
            )
            continue_button.click()
            #Время на выполнение анимации
            sleep(1.5)
        except Exception as e:
            print(f"continue PAY \{e}")

        try:
            driver.find_element(By.XPATH, '/html/body/div/div/div/div/div/span').click()
        except:
            pass

        try:
            three_months = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="premium-data-trigger"]/div[3]/div[3]/div[2]/div[2]/div[2]'))
            )
            three_months.click()
            #Время на выполнение анимации
            sleep(1.5)
        except Exception as e:
            print(f"3 months error \n {e}")

        try:
            continue_button_two = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="premium-data-trigger"]/div[3]/div[3]/div[3]/div[6]'))
            )
            continue_button_two.click()
            #Время на выполнение анимации
            sleep(1.5)
        except Exception as e:
            print(f"button contimue two \n{e}")

        driver.execute_script("window.scrollTo(0, 0);")

        try:
            sign_in = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="premium-data-trigger"]/div[3]/div[4]/div/div/div[2]/div[2]/div[2]/span'))
            )
            sign_in.click()
            #Время на выполнение анимации
            sleep(1.5)
        except Exception as e:
            print(f"SIGN IN ERROR \n{e}")

        try:
            input_email = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="signupformbuy-email"]'))
            )
            input_email.send_keys(user_login)

            input_password = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="signupformbuy-password"]'))
            )
            input_password.send_keys(user_password)

            done_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="login-form"]/div[3]'))
            )
            done_button.click()
        except Exception as e:
            print(f"INPUT ERROR \n{e}")

        try:
            choose_tron = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="select2-currency-container"]'))
            )
            choose_tron.click()
            actions = ActionChains(driver)
            for _ in range(10):
                actions.send_keys(Keys.ARROW_DOWN).perform()
                sleep(0.5)

            actions.send_keys(Keys.ENTER).perform()
        except Exception as e:
            print(f"CHOOSE TRON \n{e}")
        sleep(3)
        amount = driver.find_element(By.XPATH, '//*[@id="amount"]').get_attribute('value').replace("USDT", '')
        address = driver.find_element(By.XPATH, '//*[@id="address"]').get_attribute('value')

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }

def wallet():
    wallet = login()
    return jsonify(wallet)

