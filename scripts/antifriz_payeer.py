import requests
from time import sleep
from flask import Flask
from flask import jsonify
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#CONSTANS

app = Flask(__name__)
url = 'https://antifriz.tv/'
user_login = 'kiracase34@gmail.com'
user_password = 'oleg123'

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

#API CONSTANS

API_KEY = '7f728c25edca4f4d0e14512d756d6868'
API_URL = 'http://rucaptcha.com/in.php'
API_RESULT_URL = f'http://rucaptcha.com/res.php?key={API_KEY}&action=get'

#CHROME OPTIONS

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

#driver = webdriver.Chrome(options=chrome_options, seleniumwire_options=proxy_options)

def login(driver):
    try:
        driver.get('https://antifriz.tv/login')
        driver.maximize_window()
        print("LOGIN START")
        #Вводим логин

        element_start__input_user_login = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="email"]'))
        )
        element_start__input_user_login.send_keys(user_login)

        #Вводим пароль

        input_user_password = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]'))
        )
        input_user_password.send_keys(user_password)

        #Заходим

        accept_registration = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div[1]/div/form/button'))
        )
        accept_registration.click()

        print("LOGIN SUCCEFUL")

    except Exception as e:
        print(f"LOGIN ERROR -- \n{e}")

def get_wallet_data():
    try:
        with webdriver.Chrome(options=chrome_options, seleniumwire_options=proxy_options) as driver:
            login(driver)
            print("WALLET DATA ERROR")

            driver.get('https://antifriz.tv/payments')

            try:
                driver.find_element(By.XPATH, '//*[@id="jivo_close_button"]/jdiv').click()
            except:
                pass

            method_of_payment_payeer = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[1]/div/div[2]/form/div/div[1]/div/div[4]'))
            )
            method_of_payment_payeer.click()

            try:
                driver.implicitly_wait(10)
                send_minimal_count = driver.find_element(By.XPATH, '//*[@id="amountInput"]')
                send_minimal_count.clear()
                send_minimal_count.send_keys('5')
            except:
                print(f"SET MINIMAL VALUE ERROR \n{e}")

            try:
                driver.implicitly_wait(10)
                pay_ = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/div[1]/div/div[2]/form/div/div[3]/button')
                driver.execute_script("arguments[0].click();", pay_)
            except Exception as e:
                print(f"PAY BUTTON ERROR \n{e}")

            sleep(5)
            new_window = driver.window_handles[1]
            driver.switch_to.window(new_window)

            try:
                driver.implicitly_wait(10)
                choose_tether = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]/ul[1]/li[4]/div')
                driver.execute_script("arguments[0].click();", choose_tether)
            except Exception as e:
                print(f"ERROR CHOOSE TETHER \n{e}")

            try:
                driver.implicitly_wait(10)
                input_email = driver.find_element(By.XPATH, '//*[@id="id_order_email"]')
                input_email.clear()
                input_email.send_keys(user_login)
            except Exception as e:
                print(f"INPUT EMAIL ERROR \n{e}")

            try:
                driver.implicitly_wait(10)
                confirm = driver.find_element(By.XPATH, '/html/body/div/form/div[2]/div[4]/div[2]/a')
                driver.execute_script("arguments[0].click();", confirm)
            except Exception as e:
                print(f"CONFIRM ERROR \n{e}")

            amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="info_bitcoin"]/div[1]/h3/font[1]'))
            )
            amount = amount.text.replace("USDT", "")

            address = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="info_bitcoin"]/div[1]/h3/font[2]'))
            )
            address = address.text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
    except Exception as e:
        print(f"GET WALLET ERROR \n{e}")
        return None

@app.route('/api/selenium/antifriz')
def wallet():
    wallet_data = get_wallet_data()
    return jsonify(wallet_data)


if __name__ == "__main__":
    app.run(use_reloader = False, debug=True, port=5013)