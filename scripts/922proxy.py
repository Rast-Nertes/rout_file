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

#PAYMENTARS

user_login = 'kiracase34@gmail.com'
user_password = 'kiramira123!'
url = 'https://www.seoclerk.com'


#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False


def login(driver):
    driver.get('https://922proxy.com/login.html')
    driver.maximize_window()
    driver.execute_script("window.scrollBy(0, 350);")

    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="username"]'))
        )
        email_input.send_keys(user_login)

        pass_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]'))
        )
        pass_input.send_keys(user_password)

        log_in = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div[1]/div[2]/div[2]/div[6]/div[1]'))
        )
        log_in.click()

        #Подождем, пока появится всплывающее окно
        try:
            sleep(2)
            driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div[1]').click()
        except Exception as e:
            print(f"Не получилось кликнуть. \n{e}")
        sleep(3)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        driver.get('https://922proxy.com/meal.html')
        try:
            choose_traff = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div[9]/div[1]/div[1]/div[1]/div/p[4]'))
            )
            choose_traff.click()
            #Анимация прокрутки страницы
            sleep(2)
            driver.execute_script("window.scrollBy(0, 100);")
        except Exception as e:
            print(f"TARIFF ERROR \n{e}")

        try:
            crypto_currency = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[1]/div[2]/div[3]/div[1]'))
            )
            crypto_currency.click()

            continue_to_pay_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[3]/div[1]/div[2]/div[3]/div[2]/div[2]/div/div[1]'))
            )
            continue_to_pay_button.click()
        except Exception as e:
            print(f"CRYPTO CURRENCY ERROR \n{e}")

        sleep(5)
        new_window = driver.window_handles[1]
        driver.switch_to.window(new_window)

        address = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//p[@class="address-ph"]'))
        )
        address = address.text.replace("USDT", "")

        amount = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//p[@class="total-money"]'))
        )
        amount = amount.text

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
