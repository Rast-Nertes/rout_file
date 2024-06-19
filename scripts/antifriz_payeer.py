from time import sleep
from flask import jsonify
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://antifriz.tv/'
user_login = 'kiracase34@gmail.com'
user_password = 'oleg123'

#PROXY_CONSTANS

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}

#CHROME OPTIONS

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False
chrome_options.add_argument('--disable-blink-features=AutomationControlled')


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

            driver.get('https://antifriz.tv/payments')

            try:
                driver.find_element(By.XPATH, '//*[@id="jivo_close_button"]/jdiv').click()
            except:
                pass

            sleep(5)

            method_of_payment_payeer = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/main/div/div/div[1]/div/div[2]/form/div/div[1]/div/div[6]'))
            )
            method_of_payment_payeer.click()

            try:
                driver.implicitly_wait(10)
                send_minimal_count = driver.find_element(By.XPATH, '//*[@id="amountInput"]')
                send_minimal_count.clear()
                send_minimal_count.send_keys('5')
            except Exception as e:
                print(f"SET MINIMAL VALUE ERROR \n{e}")

            try:
                driver.implicitly_wait(10)
                pay_ = driver.find_element(By.XPATH, '//*[@id="app"]/main/div/div/div[1]/div/div[2]/form/div/div[3]/button')
                driver.execute_script("arguments[0].click();", pay_)
            except Exception as e:
                print(f"PAY BUTTON ERROR \n{e}")

            sleep(5)
            windows = driver.window_handles
            for window in windows:
                sleep(1.5)
                driver.switch_to.window(window)
                if "aye" in driver.title:
                    break

            try:
                driver.implicitly_wait(10)
                choose_tether = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]/ul[1]/li[4]')
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
            amount = amount.text.replace("USDT", "").replace(' ', '')

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
        return {'status':"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet_data()
    print(wallet_data)
    return jsonify(wallet_data)
