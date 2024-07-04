from selenium import webdriver
from time import sleep
from flask import Flask, jsonify
from fake_useragent import UserAgent
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#Coinpal

#CONSTANS

user_login = 'kiracase34@gmail.com'
user_password = 'kirakira1234'
url = 'https://www.mmoexp.com/Fc-24/Coins.html'

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
# options.add_argument("--headless")
options.headless = False


def login(driver):
    driver.get(url)
    driver.maximize_window()
    print("START LOGIN")

    sleep(3)
    try:
        find_log_but = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//span[@class="sing user current jq-user"]'))
        )
        find_log_but.click()
    except Exception as e:
        print(f'ERROR CLICK LOG BUT \n{e}')

    try:
        find_log_input = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '(//input[@type="text"])[2]'))
        )
        find_log_input.send_keys(user_login)

        sleep(0.5)

        find_pass_input = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '(//input[@type="password"])[1]'))
        )
        find_pass_input.send_keys(user_password)
    except Exception as e:
        print(f'ERROR INPUT LOG DATA \n{e}')

    sleep(1)
    try:
        log_but = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/header/ul[1]/li[6]/span'))
        )
        log_but.click()
    except Exception as e:
        print(f'ERROR CLICK LOG BUTT \n{e}')

    input("press")
    print("LOGIN SUCCEFULY")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        print("START GET WALLET")
        try:
            driver.implicitly_wait(10)
            but_now_button = driver.find_element(By.XPATH, '//*[@id="butNow"]')
            driver.execute_script("arguments[0].click();", but_now_button)

            try:
                driver.implicitly_wait(10)
                input_count = driver.find_element(By.XPATH, '/html/body/header/div[2]/ul/ul/li/div/div[2]/div/input')
                input_count.clear()
                input_count.send_keys('1')
            except Exception as e:
                print(f"INPUT COUNT ERROR \n{e}")

            driver.implicitly_wait(10)
            checkout_button = driver.find_element(By.XPATH, '/html/body/header/div[2]/div/a')
            driver.execute_script("arguments[0].click();", checkout_button)
        except Exception as e:
            print(f"PAY BUTTON ERROR \n{e}")
            return None

        try:
            driver.implicitly_wait(10)
            email_input_for_pay = driver.find_element(By.XPATH, '//*[@id="app"]/form/div[1]/div/div[1]/section[2]/div[2]/form/div[1]/div/div/div[1]/input')
            email_input_for_pay.send_keys(user_login)

            driver.implicitly_wait(10)
            pass_input_for_pay = driver.find_element(By.XPATH, '//*[@id="app"]/form/div[1]/div/div[1]/section[2]/div[2]/form/div[2]/div/div/div[1]/input')
            pass_input_for_pay.send_keys(user_password)

            driver.implicitly_wait(10)
            backup_code1 = driver.find_element(By.XPATH, '//*[@id="app"]/form/div[1]/div/div[1]/section[2]/div[2]/form/div[3]/div/div/div[1]/input')
            backup_code1.send_keys('11111111')

            driver.implicitly_wait(10)
            backup_code2 = driver.find_element(By.XPATH,'//*[@id="app"]/form/div[1]/div/div[1]/section[2]/div[2]/form/div[4]/div/div/div[1]/input')
            backup_code2.send_keys('11111111')

            driver.implicitly_wait(10)
            backup_code3 = driver.find_element(By.XPATH, '//*[@id="app"]/form/div[1]/div/div[1]/section[2]/div[2]/form/div[5]/div/div/div[1]/input')
            backup_code3.send_keys('11111111')

            driver.implicitly_wait(10)
            ticket = driver.find_element(By.XPATH, '//*[@id="app"]/form/div[1]/div/div[1]/section[3]/div/div[1]/input')
            driver.execute_script("arguments[0].click();", ticket)
        except Exception as e:
            print(f"DATA INPUT ERROR \n{e}")

        print("GET WALLET CONTINUE...")

        try:
            driver.implicitly_wait(10)
            choose_crypto_payment = driver.find_element(By.ID, 'method-coinpal')
            driver.execute_script("arguments[0].click();", choose_crypto_payment)
        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")

        try:
            #Анимация для появления кнопки
            sleep(5)
            pay_now_before_choose_wallet = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/main/div[3]/form/div[1]/div/div[2]/section/ul[2]/li[3]/input'))
            )
            pay_now_before_choose_wallet.click()

        except Exception as e:
            print(f"PAY NOW BEFORE CHOOSE WALLET \n{e}")

        try:
            driver.implicitly_wait(10)
            new_window = driver.window_handles[1]
            driver.switch_to.window(new_window)

            driver.implicitly_wait(30)
            choose_usdt_trc20 = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div[2]')
            driver.execute_script("arguments[0].click();", choose_usdt_trc20)

        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")

        try:
            amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="__layout"]/div/div/div/div/div[1]/div/div[7]/div[1]/div[2]/span[1]'))
            )
            amount = amount.text

            address = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="__layout"]/div/div/div/div/div[2]/div[1]/div[5]/div[1]/div/div[1]/div[4]/span'))
            )
            address = address.text
            print("DATA SUCCEFULY")
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
