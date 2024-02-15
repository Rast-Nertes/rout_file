from time import sleep
from flask import Flask
from flask import jsonify
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path
from selenium.webdriver.common.keys import Keys

#CONSTANS

app = Flask(__name__)
url = 'https://xvpn.io/ru'
user_login = 'kiracase34@gmail.com'
user_password = 'Oleg7711!'

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

#CHROME OPTIONS

#driver_path = Path('C:\\Users\\Acer\\Desktop\\python_work\\web_drivers\\chromedriver.exe')

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--headless")

def login(driver):
    try:
        print("LOGIN START")
        driver.get('https://xvpn.io/ru/login')
        sleep(1.5)
        driver.maximize_window()
        #Вводим логин
        element_start__input_user_login = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/main/div[2]/div[1]/div[1]/input'))
        )
        element_start__input_user_login.send_keys(user_login)
        #Вводим пароль
        input_user_password = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[2]/input')
        input_user_password.send_keys(user_password)

        accept_registration = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/main/div[2]/div[1]/div[3]'))
        )

        accept_registration.click()

        sleep(15)
        print("LOGIN SUCCEFUL")
    except Exception as e:
        print(f"LOGIN ERROR -- {e}")
        return None

def wallet_data():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)
        try:
            print("WALLET START")
            #Переходим на страницу, где есть траффики, выбираем минимальный
            driver.get('https://xvpn.io/ru/pricing')
            element_to_start__choice_traffic = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/section[2]/ul/li[2]'))
            )
            element_to_start__choice_traffic.click()
            element_to_start__choice_traffic.click()
            sleep(1.5)

            #Выбираем способ оплаты
            choice_way = driver.find_element(By.XPATH, '/html/body/main/div/section[4]/div[2]/div[1]/div[3]/div[1]')
            choice_way.click()

            accept_way = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/main/div/section[4]/div[2]/div[1]/div[3]/div[2]/div[6]/div[1]'))
            )
            accept_way.click()
            sleep(10)
            print(1)
            driver.refresh()
            driver.execute_script("window.scrollBy(0, 1000);")
            print("WALLET SUCCEFUL")
        except Exception as e:
            print(f"WALLET ERROR -- {e}")
            return None

        try:
            currency = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="btn_USDT.TRC20"]'))
            )
            currency.click()

            accept_currency = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="btnCheckout"]'))
            )
            accept_currency.click()

            try:
                sleep(10)
                address = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="email-form"]/div[2]/div[1]/div[3]/div[2]'))
                )
                address = address.text

                amount = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="email-form"]/div[2]/div[1]/div[1]/div[2]'))
                )
                amount = amount.text.replace('USDT.TRC20', '')

                return {
                    "address": address,
                    "amount": amount,
                    "currency": "usdt"
                }
            except Exception as e:
                print(f"DATA ERROR \n{e}")
        except Exception as e:
            print(f"RESULT ERROR -- {e}")

def wallet():
    wallet = wallet_data()
    print(wallet)
    return jsonify(wallet)

