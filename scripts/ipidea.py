from seleniumwire import webdriver
from time import sleep
from flask import Flask, jsonify
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

#Paymentmars

#CONSTANS


url = 'https://www.ipidea.io/userLogin'
user_login = 'kiracase34@gmail.com'
user_password = 'oleg123567'

#API CONSTANS

API_KEY = '7f728c25edca4f4d0e14512d756d6868'
API_URL = 'http://rucaptcha.com/in.php'
API_RESULT_URL = f'http://rucaptcha.com/res.php?key={API_KEY}&action=get'

#CHROME OPTIONS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.headless = False
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

#PROXY_CONSTANS

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
    driver.maximize_window()

    try:
        input_email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div/div[1]/div/div[2]/form/div[1]/div/div/input'))
        )
        input_email.send_keys(user_login)

        input_pass = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div/div[1]/div/div[2]/form/div[2]/div/div/input'))
        )
        input_pass.send_keys(user_password)

        button_log_in = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div/div[1]/div/div[2]/form/div[3]/div/button[1]'))
        )
        button_log_in.click()
    except Exception as e:
        print(f'ERROR INPUT \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        sleep(4)
        new_window = driver.window_handles[1]
        driver.switch_to.window(new_window)
        try:
            close_ = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div[1]'))
            )
            close_.click()
        except Exception as e:
            pass

        try:
            close_2 = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[3]/div[2]/div'))
            )
            close_2.click()
        except:
            pass

        try:
            select_traffic = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="paneContent"]/div[2]/div[2]/p[5]'))
            )
            select_traffic.click()
        except Exception as e:
            print(f"SELECT ERROR \n{e}")

        try:
            choose_payment = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div/div[2]/div[2]/div/div/div[2]/div[3]/div[2]/div[1]/div[1]'))
            )
            choose_payment.click()
            driver.execute_script("window.scrollBy(0, 350);")

            submit_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div/div[2]/div[2]/div/div/div[2]/div[5]/div'))
            )
            submit_button.click()
        except Exception as e:
            print(f"ERROR CHOOSE PAYMENT \n{e}")

        sleep(7.5)
        windows = driver.window_handles
        for window in windows:
            driver.switch_to.window(window)
            tittle = driver.title
            print(tittle)
            sleep(1)
            if "mars" in tittle:
                break

        amount = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="__layout"]/div/div[1]/div[1]/div[2]/div/div[2]/div[3]/div[2]/div[1]/div[3]'))
        )
        amount = amount.text.replace("USDT", '').replace(" ", '')

        address = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="__layout"]/div/div[1]/div[1]/div[2]/div/div[2]/div[3]/div[1]/div[1]/div[2]'))
        )
        address = address.text

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
