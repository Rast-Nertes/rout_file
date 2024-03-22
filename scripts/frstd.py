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

url = 'https://frstd.ru/item/kupit-proxy'
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
        input_email = driver.find_element(By.CSS_SELECTOR, 'div.panel-footer > div:nth-child(1) > div:nth-child(4) > input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'div.panel-footer > div:nth-child(1) > div:nth-child(2) > input')
        input_password.clear()
        input_password.send_keys('1')

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[1]/div[2]/div[1]/div/div/div/span/div[3]/div[1]/div[5]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        sleep(3)
        driver.switch_to.window(driver.window_handles[1])

        try:
            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[8]/div/div')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"ERROR CHOOSE TRC20 \n{e}")

        try:
            driver.implicitly_wait(30)
            input_email = driver.find_element(By.ID, 'email')
            input_email.clear()
            input_email.send_keys(user_email)

            driver.implicitly_wait(10)
            submit_button = driver.find_element(By.CSS_SELECTOR, 'button.btn.btn-primary.btn-sign.me-md-2.mb-2.mb-md-0 > span:nth-child(1)')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit_button)
        except Exception as e:
            print(f"ERROR INPUT EMAIL \n{e}")

        try:
            driver.implicitly_wait(10)
            amount = driver.find_element(By.ID, 'amount').get_attribute('value')

            driver.implicitly_wait(10)
            address = driver.find_element(By.ID, 'address').get_attribute('value')

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
