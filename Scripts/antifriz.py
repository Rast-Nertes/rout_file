import requests
from seleniumwire import webdriver
from time import sleep
from flask import Flask, jsonify
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha
from selenium.webdriver.common.by import By

# CryptoCloud

# CONSTANS
app = Flask(__name__)
user_login = 'kiracase34@gmail.com'
user_password = 'oleg123'
url = 'https://antifriz.tv/login'

# API CONSTANS
API_KEY = '7f728c25edca4f4d0e14512d756d6868'
# API_URL = 'http://rucaptcha.com/in.php'
# API_RESULT_URL = f'http://rucaptcha.com/res.php?key={API_KEY}&action=get'

# PROXY_CONSTANS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy": {
        "http": f"http://{proxy_login}:{proxy_password}@45.130.254.133:8000",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}

# CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.headless = False


def solve_captcha(sitekey: str, url: str) -> str:
    solver = TwoCaptcha(API_KEY)
    result = solver.recaptcha(sitekey=sitekey, url=url, invisible=1)
    return result["code"]


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(20)
        input_email = driver.find_element(By.XPATH, '//*[@id="email"]')
        input_email.send_keys(user_login)

        driver.implicitly_wait(20)
        input_password = driver.find_element(By.XPATH, '//*[@id="password"]')
        input_password.send_keys(user_password)
    except Exception as e:
        print(f'ERROR INPUT \n{e}')

    driver.implicitly_wait(50)
    captcha_code = solve_captcha('6LdBtr4aAAAAACrQ8Wu4Yav061NabdPIzv5I1lds', url)
    driver.execute_script(
        f'var textarea = document.getElementById("g-recaptcha-response-100000"); textarea.style.display = "block"; textarea.innerHTML = "{captcha_code}";')

    try:
        driver.implicitly_wait(20)
        login_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/form/button')
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN BUTTON ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)
        driver.get('https://antifriz.tv/payments')

        try:
            driver.implicitly_wait(10)
            choose_cryptocloud = driver.find_element(By.XPATH,
                                                     '//*[@id="app"]/main/div/div/div[1]/div/div[2]/form/div/div[1]/div/div[5]')
            driver.execute_script("arguments[0].click();", choose_cryptocloud)

            driver.implicitly_wait(20)
            input_money = driver.find_element(By.XPATH, '//*[@id="amountInput"]')
            input_money.clear()
            input_money.send_keys('1')

            try:
                sleep(3)
                driver.implicitly_wait(10)
                add_balance = driver.find_element(By.XPATH,
                                                  '//*[@id="app"]/main/div/div/div[1]/div/div[2]/form/div/div[3]/button')
                driver.execute_script("arguments[0].click();", add_balance)
            except Exception as e:
                print(f"PAY BUTTON ERROR \n{e}")

        except Exception as e:
            print(f"CHOOSE AND INPUT ERROR \n{e}")
            sleep(1000)

        sleep(5)
        new_window = driver.window_handles[1]
        driver.switch_to.window(new_window)

        try:
            # Пожалуй, это самый лучший способ со слипом
            pay_ = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div[3]/button/span/div/img'))
            )
            driver.execute_script("arguments[0].click();", pay_)
        except Exception as e:
            print(f"PAY BUTTON ERROR \n{e}")
            sleep(100)

        try:
            amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH,
                     '/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/span'))
            )
            amount = amount.text.replace(' USDT', '')
        except Exception as e:
            print(f"ERROR AMOUNT \n{e}")

        address = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 '/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div/span'))
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
    return wallet_data

if __name__ == "__main__":
    wallet()
