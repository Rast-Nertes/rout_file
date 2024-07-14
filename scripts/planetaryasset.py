from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://planetaryasset.io/?a=login'
user_email = "alex37347818"
user_password = "3yxbYzren2q5Uw@"

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.add_experimental_option("detach", True)


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        click_me_button = driver.find_element(By.XPATH, '//button[@id="clickbutton"]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", click_me_button)
    except Exception as e:
        print(f"CLICK ME BUTTON ERROR \n{e}")


    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.CSS_SELECTOR, 'form > div > div.rinformation > div:nth-child(2) > div.infotype > input[type=text]')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'form > div > div.rinformation > div:nth-child(3) > div.infotype > input[type=password]')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'form > div > div.agree_create > div.btnsubmita > input[type=submit]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        sleep(7.5)
        driver.get('https://planetaryasset.io/?a=deposit')

        try:
            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.CSS_SELECTOR, 'div > div.spendall > div:nth-child(13) > div.check_paymenta > input[type=radio]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(10)
            spend_button = driver.find_element(By.CSS_SELECTOR, 'div > div.spendall > div.spendnow > input[type=submit]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", spend_button)
        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(40)
            address = driver.find_element(By.CSS_SELECTOR, '#usdt\.trc20_form > i > a').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, '#usdt\.trc20_form > b').text.replace("USDT.TRC20", "").replace(" ", "")

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
