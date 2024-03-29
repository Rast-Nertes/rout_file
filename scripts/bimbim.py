import pyautogui
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
#form_token_login
url = 'https://bimbim.com/ru/auth/login'
user_email = "Spongegege"
user_email_ = 'kiracase34@gmail.com'
user_password = "Qwerty62982"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        accept_cookie = driver.find_element(By.XPATH, '//*[@id="react-app"]/div/div[2]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", accept_cookie)
    except:
        pass

    try:
        driver.implicitly_wait(50)
        input_email = driver.find_element(By.XPATH, '//*[@id="login"]/form/div[1]/input')
        sleep(1.5)
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(30)
        input_password = driver.find_element(By.XPATH, '//*[@id="login"]/form/div[2]/input')
        sleep(1.5)
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.ID, 'submit_text')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        close = driver.find_element(By.XPATH, '//*[@id="gift-promo"]/div/div/div/span')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", close)
    except Exception as e:
        pass
    sleep(5)
    driver.get('https://bimbim.com/ru/free/payment')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(60)
            buy_credits = driver.find_element(By.XPATH, '//*[@id="overlay-container"]/section/div/div[2]/div[1]/div[1]/div/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_credits)
        except Exception as e:
            print(f"ERROR BUY CREDITS \n{e}")

        try:
            driver.implicitly_wait(60)
            choose_crypto = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/ul/li[3]/form/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_crypto)

            driver.implicitly_wait(40)
            buy_cr = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/form[1]/div/div[2]/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_cr)
        except Exception as e:
            print(f"ERROR CHOOSE CRYPTO \n{e}")

        try:
            driver.implicitly_wait(20)
            choose_usdt = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div/label[8]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_usdt)

            driver.implicitly_wait(20)
            continue_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button)
        except Exception as e:
            print(f"ERROR CHOOSE USDT \n{e}")

        try:
            driver.implicitly_wait(50)
            input_email = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[1]/form/div/div[2]/input')
            sleep(1.5)
            input_email.click()
            sleep(1.5)
            pyautogui.write(user_email_)

            driver.implicitly_wait(20)
            continue_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[2]/div/div[2]/div/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button)

            driver.implicitly_wait(50)
            choose_tron = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[3]/div/div/label[3]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_tron)

            driver.implicitly_wait(50)
            continue_button_2 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div[2]/div/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button_2)
        except Exception as e:
            print(f"ERROR CHOOSE TRON \n{e}")

        driver.set_window_size(1200, 500)

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            amount = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/p').text.replace("USDT", '').replace(" ", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[6]/div/div[2]/div/p').text

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