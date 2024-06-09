import time

import cloudscraper
from seleniumwire import webdriver
from flask import Flask, jsonify
from fake_useragent import UserAgent
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#Coingate

user_login = 'nobrandnametoshow@gmail.com'
user_password = 'kiramira123'
url = 'https://premiumkey.co/account/login'

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False


proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        input_email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="input-email"]'))
        )
        input_email.send_keys(user_login)

        input_password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="input-password"]'))
        )
        input_password.send_keys(user_password)

        try:
            button_to_login = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div[2]/div/form/input'))
            )
            button_to_login.click()
        except Exception as e:
            print(f"BUTTON TO LOG IN \n{e}")

    except Exception as e:
        return {"status":"0", "ext":f"error login {e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        driver.get('https://premiumkey.co/premium-key/dasan-paypal-reseller')

        try:
            button_buy = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="Placeorder"]/div[2]/a'))
            )
            button_buy.click()

        except Exception as e:
            print(f"BUTTON BUY ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_wallet = driver.find_element(By.XPATH, '//*[@id="coingate"]/label')
            time.sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_wallet)

            driver.implicitly_wait(10)
            ticket = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/input')
            time.sleep(1.5)
            driver.execute_script("arguments[0].click();", ticket)

            time.sleep(3.5)

            driver.implicitly_wait(10)
            checkout_button = driver.find_element(By.XPATH, '//*[@id="button-loggedorder"]')
            driver.execute_script("arguments[0].click();", checkout_button)

            try:
                driver.implicitly_wait(10)
                confirm_order_button = driver.find_element(By.XPATH, '//*[@id="button-confirm"]')
                driver.execute_script("arguments[0].click();", confirm_order_button)
            except Exception as e:
                print(f"CONFIRM BUTTON ERROR ")
        except Exception as e:
            return {"status":"0", "ext":f"error wallet  {e}"}

        try:
            driver.implicitly_wait(10)
            choose_tether = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div/label[10]')
            driver.execute_script("arguments[0].click();", choose_tether)

            driver.implicitly_wait(10)
            continue_payment = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/button')
            driver.execute_script("arguments[0].click();", continue_payment)
        except Exception as e:
            print(f"ERROR CHOOSE \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_network = driver.find_element(By.CSS_SELECTOR, 'div.short-background.css-10h2p0h.e1wz9m0w0 > div.css-nl7kme.e7kd91g2 > div > div > label:nth-child(3)')
            driver.execute_script("arguments[0].click();", choose_network)

            driver.implicitly_wait(10)
            continue_choose_network = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div[2]/div/button[1]')
            driver.execute_script("arguments[0].click();", continue_choose_network)
        except Exception as e:
            print(f"continue without email error \n{e}")

        try:
            input_email = driver.find_element(By.XPATH, '//input[@name="email"]')
            time.sleep(1.5)
            input_email.send_keys(user_login)

            click_continue_button = driver.find_element(By.XPATH, '(//button[@type="button"])[5]')
            time.sleep(1.5)
            click_continue_button.click()
        except Exception as e:
            print(f'ERROR INPUT EMAIL \n{e}')

        try:
            driver.set_window_size(1000, 750)

            amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/p'))
            )
            amount = amount.text.replace("USDT", "")

            address = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[6]/div/div[2]/div/p'))
            )
            address = address.text

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