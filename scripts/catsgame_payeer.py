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

url = 'https://catsgame.fun'
user_login = "kiracase34"
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
#options.add_argument("--headless")


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.CSS_SELECTOR, 'div.col-lg-6.pl-md--2.pr-md--2.mt-sm--3 > div > form > div > div.col-lg-8.mb-2 > center > input:nth-child(1)')
        sleep(1.5)
        input_email.clear()
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'div.col-lg-6.pl-md--2.pr-md--2.mt-sm--3 > div > form > div > div.col-lg-8.mb-2 > center > input:nth-child(2)')
        sleep(1.5)
        input_password.clear()
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"INPUT DATA LOGIN ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        button_login = driver.find_element(By.CSS_SELECTOR, 'div.col-lg-6.pl-md--2.pr-md--2.mt-sm--3 > div > form > div > div.col-lg-8.mb-2 > center > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", button_login)
    except Exception as e:
        print(f"BUTTON LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        driver.get('https://catsgame.fun/user/insert')

        try:
            driver.implicitly_wait(10)
            input_sum = driver.find_element(By.CSS_SELECTOR, 'div.col-lg-6.pl-md--2.pr-md--2.mt-sm--3 > div > main > div > div > div > div > div.row > div:nth-child(1) > form > div:nth-child(2) > input')
            sleep(1.5)
            input_sum.clear()
            input_sum.send_keys('550')

            driver.implicitly_wait(10)
            btn_success = driver.find_element(By.CSS_SELECTOR, 'div.col-lg-6.pl-md--2.pr-md--2.mt-sm--3 > div > main > div > div > div > div > div.row > div:nth-child(1) > form > div:nth-child(3) > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", btn_success)

            driver.implicitly_wait(10)
            accept_btn = driver.find_element(By.CSS_SELECTOR, 'div.col-lg-6.pl-md--2.pr-md--2.mt-sm--3 > div > main > div > div > div > div > center > div > form > input.btn.btn-success')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", accept_btn)
        except Exception as e:
            print(f"BTN SUCCESS ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_usdt = driver.find_element(By.CSS_SELECTOR, 'div.container > div.slist > ul:nth-child(3) > li:nth-child(3) > div')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_usdt)

            driver.implicitly_wait(10)
            input_email = driver.find_element(By.ID, 'id_order_email')
            input_email.clear()
            input_email.send_keys(user_email)

            driver.implicitly_wait(10)
            accept_choose = driver.find_element(By.CSS_SELECTOR, 'div.container > div.footer > div.foot-half.to-right > a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", accept_choose)
        except Exception as e:
            print(f"CHOOSE USDT ERROR \n{e}")

        try:
            driver.implicitly_wait(40)
            address = driver.find_element(By.CSS_SELECTOR, 'div.amount__info.bb-info.attantion.blue-atantion > h3 > font:nth-child(6)').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, 'div.amount__info.bb-info.attantion.blue-atantion > h3 > font:nth-child(4)').text.replace("USDT", "").replace(" ", "")

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
