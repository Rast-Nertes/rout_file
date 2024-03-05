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
            input_sum = driver.find_element(By.ID, 'billingPaySum')
            input_sum.clear()
            input_sum.send_keys("550")
        except Exception as e:
            print(f"ERROR INPUT SUM \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_freekassa = driver.find_element(By.ID, 'freekassa')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_freekassa)
            sleep(2)

            driver.implicitly_wait(10)
            pay_hundred = driver.find_element(By.ID, 'billingPayBtn')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", pay_hundred)
        except Exception as e:
            print(f"ADD BALANCE ERROR \n{e}")

        print("Balance passed")

        try:
            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.ID, 'currency-15')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            print("Choose passed")

            driver.implicitly_wait(10)
            input_email = driver.find_element(By.XPATH, '//*[@id="pay-global"]/div/div[1]/div/form/div/div[2]/input')
            input_email.clear()
            input_email.send_keys(user_email)
        except Exception as e:
            print(f"INPUT EMAIL \n{e}")

        try:
            driver.implicitly_wait(10)
            submit_payment = driver.find_element(By.ID, 'submit-payment')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit_payment)
        except Exception as e:
            print(f"SUBMIT ERROR \n{e}")

        input("Press")

        try:
            driver.implicitly_wait(40)
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
