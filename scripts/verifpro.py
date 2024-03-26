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
url = 'https://verifpro.net/products/info/259341'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(30)
        buy_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[1]/div/div/div/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", buy_button)
    except Exception as e:
        print(f"ERROR BUY BUTTON ERROR \n{e}")

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.ID, 'emailBuy')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(20)
        pay_send = driver.find_element(By.ID, 'setEmailButton')
        sleep(1.5)
        driver.execute_script('arguments[0].click();', pay_send)
    except Exception as e:
        print(f"ERROR INPUT DATA \n{e}")

    try:
        driver.implicitly_wait(60)
        input_email_plisio = driver.find_element(By.ID, 'form_emailStep__email')
        input_email_plisio.clear()
        input_email_plisio.send_keys(user_email)

        driver.implicitly_wait(20)
        next_step = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[2]/form/div[2]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", next_step)
    except Exception as e:
        print(f"ERROR NEXT STEP \n{e}")

    try:
        driver.implicitly_wait(30)
        choose_tether = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[3]/div[13]/button/div')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", choose_tether)

        driver.implicitly_wait(20)
        choose_trc20 = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[3]/div[2]/button/div')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", choose_trc20)
    except Exception as e:
        print(f"ERROR CHOOSE \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(5.5)
            driver.implicitly_wait(10)
            amount = driver.find_element(By.ID, 'step_pay__amount_payTo').text

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[7]').text

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
