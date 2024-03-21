from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://rt.pornhubpremium.com/premium/login'
user_email = "kiracase34@gmail.com"
user_password = "KIRAmira123123!"
api_ = '7f728c25edca4f4d0e14512d756d6868'

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    extension_path = paths[1].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_extension(extension_path)

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

    driver.switch_to.window(driver.window_handles[0])
    try:
        driver.implicitly_wait(10)
        input_api_key = driver.find_element(By.CSS_SELECTOR, 'body > div > div.content > table > tbody > tr:nth-child(1) > td:nth-child(2) > input[type=text]')
        input_api_key.clear()
        input_api_key.send_keys(api_)

        driver.implicitly_wait(5)
        connect = driver.find_element(By.ID, 'connect')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", connect)
    except Exception as e:
        print(f"ERROR CONNECT \n{e}")

    driver.switch_to.window(driver.window_handles[1])

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.ID, 'username')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.ID, 'password')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.ID, 'submitLogin')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(10)
            enter = driver.find_element(By.ID, 'closeEnterModal')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", enter)
        except Exception as e:
            print(f"ENTER ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            upgrade_link = driver.find_element(By.ID, 'premium-upgrade-link')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", upgrade_link)

            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.XPATH, '//*[@id="modalWrapMTubes"]/div/div/div/v-crypto-form/form/div[1]/div[3]/div[16]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"ERROR CHOOSE TRC20 \n{e}")

        sleep(10)

        try:
            driver.implicitly_wait(10)
            wait_sub = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/v-crypto-form/form/div[1]/div[4]/div[3]/div/div[2]')
            sleep(1.5)
            wait_sub.click()
        except Exception as e:
            print(f"ERROR SOLVE CAPTCHA \n{e}")

        try:
            while True:
                driver.implicitly_wait(5)
                captcha_result = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/v-crypto-form/form/div[1]/div[4]/div[3]/div/div[2]/div[2]').text
                if "Решается" in captcha_result:
                    sleep(5)
                    print("Капча решается...")
                else:
                    break
        except Exception as e:
            print(f"ERROR CAPTCHA \n{e}")

        try:
            driver.implicitly_wait(10)
            submit_button = driver.find_element(By.CSS_SELECTOR, 'div > v-crypto-form > form > div.formMainContent > div.submitWrapper > input')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit_button)
            sleep(3)
        except Exception as e:
            print(f"ERROR SUBMIT BUTTON \n{e}")

        try:
            sleep(3)
            driver.refresh()
            driver.implicitly_wait(60)
            amount = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]').text.replace("USDT", '').replace(" ", '').replace("TRX", '').replace("\n", '')

            driver.implicitly_wait(30)
            address = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[1]').text

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
