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

url = 'https://garantmarket.net/'
user_login = "kiracase34"
user_email = "kiracase34@gmail.com"
user_password = "@@ED2BqKyJCW6@2"

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
#options.add_argument("--headless")


def login(driver):
    driver.maximize_window()
    driver.get(url)

    try:
        driver.implicitly_wait(10)
        button_to_login = driver.find_element(By.CSS_SELECTOR, '#main_header > div > div:nth-child(3) > a > img')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", button_to_login)

        driver.implicitly_wait(10)
        input_login = driver.find_element(By.ID, 'login_name')
        sleep(1.5)
        input_login.clear()
        input_login.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.ID, 'login_password')
        sleep(1.5)
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'div > div.modal-body > form > div.row > div.col-md-3.col-sm-3.col-xs-12 > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")
    print("Login passed")
    sleep(4)


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        driver.get("https://garantmarket.net/billing.html/pay/")

        try:
            driver.implicitly_wait(10)
            choose_freekassa = driver.find_element(By.ID, 'payok')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_freekassa)
            sleep(2)

            driver.implicitly_wait(10)
            pay_hundred = driver.find_element(By.ID, 'billingPayBtn')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", pay_hundred)
        except Exception as e:
            print(f"ADD BALANCE ERROR \n{e}")

        try:
            driver.implicitly_wait(15)
            driver.find_element(By.ID, 'pay_tether_trc')
            sleep(2)

            driver.implicitly_wait(15)
            choose_tether20 = driver.find_element(By.ID, 'pay_tether_trc')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_tether20)
        except Exception as e:
            print(f"CHOOSE TETHER20 ERROR \n{e}")

        try:
            sleep(3)
            driver.implicitly_wait(10)
            input_email = driver.find_element(By.CSS_SELECTOR, '#pay_tether_trc_generate_form > fieldset.pay_input_crypto_block > input[type=email]')
            sleep(1.5)
            input_email.clear()
            input_email.send_keys(user_email)

            sleep(2)
            driver.implicitly_wait(10)
            create_address_button = driver.find_element(By.ID, 'pay_tether_trc_generate_button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", create_address_button)
        except Exception as e:
            print(f"INPUT EMAIL ERROR \n{e}")

        try:

            sleep(4)
            driver.implicitly_wait(10)
            qr_code_src = driver.find_element(By.XPATH, '/html/body/main/div[1]/div[3]/div[6]/div[2]/div[4]/div/div[2]/img').get_attribute('src')
            try:
                parts = qr_code_src.split(':')
                address = parts[2].split('?')[0]
            except Exception as e:
                print(f"ERROR DET ADDRESS \n{e}")

            driver.implicitly_wait(10)
            amount = driver.find_element(By.CSS_SELECTOR, '#pay_tether_trc_generate_form > input[type=hidden]:nth-child(7)').get_attribute('value')

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
