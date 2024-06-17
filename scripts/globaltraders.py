from flask import jsonify
import re
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://globaltraders.pro/login/'
user_login = "kiracase34"
user_email = "kiracase34@gmail.com"
user_password = "bc4-fr9-XNb-A7V"

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@45.130.254.133:8000",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def login(driver):
    driver.get(url)

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.XPATH, '//input[@name="login"]')
        input_email.clear()
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '//input[@name="password"]')
        input_password.clear()
        input_password.send_keys(user_password)
    except Exception as e:
        print(f'INPUT LOGIN ERROR \n{e}')

    try:
        driver.implicitly_wait(10)
        log_button = driver.find_element(By.CSS_SELECTOR, 'div.main-content > div > div > form > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", log_button)
    except Exception as e:
        print(f"LOGIN BUTTON ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        driver.maximize_window()
        login(driver)

        sleep(3.5)
        driver.get('https://globaltraders.pro/user/wallets/')

        try:
            driver.implicitly_wait(10)
            append_trc20 = driver.find_element(By.CSS_SELECTOR, 'div.wallets-table-wrapper > table > tbody > tr:nth-child(4) > td:nth-child(3) > div > a.button.button_type_first.button_color_yellow.wallets-table__button-down')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", append_trc20)
        except Exception as e:
            print(f"APPEND TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_sum = driver.find_element(By.CSS_SELECTOR, 'div > div.user-section__main > div.output-block > div > form > div:nth-child(4) > input')
            input_sum.clear()
            input_sum.send_keys('10')

            driver.implicitly_wait(10)
            append_sum = driver.find_element(By.ID, 'go_investmens')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", append_sum)
        except Exception as e:
            print(f"INPUT SUM ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            amount_element = driver.find_element(By.CSS_SELECTOR, 'div > div.popup-invest-block-content > div:nth-child(1) > p:nth-child(3)').text.replace("Сумма: ", "").replace(" USDT", "")
            amount_index = amount_element.find("(")
            amount = amount_element[:amount_index].strip()

            driver.implicitly_wait(10)
            address_element = driver.find_element(By.CSS_SELECTOR,'#form_investors > div:nth-child(4) > div > div > div').text
            start_index = address_element.find("Отправляете на счет: ")
            address = address_element[start_index + len("Отправляете на счет: "):].split("\n")[0].strip()

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
