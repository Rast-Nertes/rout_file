from selenium import webdriver
from time import sleep
from twocaptcha import TwoCaptcha
from flask import Flask, jsonify
from fake_useragent import UserAgent
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#Zerocryptopay

#CONSTANS
app = Flask(__name__)
user_login = 'kiracase34@gmail.com'
user_password = 'NFU*Bc@qh$64'
url = 'https://amazingrdp.com/whmcs/store/economy-cheap-plans'

#API CONSTANS
API_KEY = "7f728c25edca4f4d0e14512d756d6868"

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

driver = webdriver.Chrome(options= options)

def solve_captcha(sitekey: str, url: str) -> str:
    solver = TwoCaptcha(API_KEY)
    result = solver.recaptcha(sitekey=sitekey, url=url, invisible=1)
    return result["code"]

def get_wallet():
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        order_now_button = driver.find_element(By.XPATH, '//*[@id="product2-order-button"]')
        driver.execute_script("arguments[0].click()", order_now_button)

        driver.implicitly_wait(20)
        continue_pay = driver.find_element(By.XPATH, '//*[@id="btnCompleteProductConfig"]')
        driver.execute_script("arguments[0].click();", continue_pay)

        driver.implicitly_wait(10)
        checkout_button = driver.find_element(By.XPATH, '//*[@id="checkout"]')
        driver.execute_script("arguments[0].click();", checkout_button)
    except Exception as e:
        print(f"PAY ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        registred_button = driver.find_element(By.XPATH, '//*[@id="btnAlreadyRegistered"]')
        driver.execute_script("arguments[0].click()", registred_button)
    except Exception as e:
        print(f"REGISTRED BUTTON ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.XPATH, '//*[@id="inputLoginEmail"]')
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '//*[@id="inputLoginPassword"]')
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"LOGIN INPUT ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        choose_crypto_pay = driver.find_element(By.XPATH, '//*[@id="paymentGatewaysContainer"]/div/label[2]')
        driver.execute_script("arguments[0].click();", choose_crypto_pay)

        try:
            driver.implicitly_wait(10)
            ticket = driver.find_element(By.XPATH, '//*[@id="iCheck-accepttos"]/ins')
            driver.execute_script("arguments[0].click();", ticket)
        except Exception as e:
            print(f"TICKET ERROR \n{e}")

    except Exception as e:
        print(f"CHOOSE ERROR \n{e}")

    captcha_code = solve_captcha('6LdlrVInAAAAAOXFNy78juQlFJkcFikmnCrjZjUy', driver.current_url)
    #print(captcha_code)
    driver.execute_script(f'var textarea = document.getElementById("g-recaptcha-response"); textarea.style.display = "block"; textarea.innerHTML = "{captcha_code}";')

    try:
        driver.implicitly_wait(10)
        complete_order = driver.find_element(By.XPATH, '//*[@id="btnCompleteOrder"]')
        driver.execute_script("arguments[0].click();", complete_order)
    except Exception as e:
        print(f"COMPLETE ORDER BUTTON \n{e}")
        return None

    try:
        driver.implicitly_wait(20)
        choose_tether = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div/label[10]')
        driver.execute_script("arguments[0].click();", choose_tether)

        driver.implicitly_wait(10)
        continue_choose_tether = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/button')
        driver.execute_script("arguments[0].click();", continue_choose_tether)

        try:
            driver.implicitly_wait(20)
            continue_without_email_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[1]/div[2]/button[2]')
            driver.execute_script("arguments[0].click();", continue_without_email_button)
        except Exception as e:
            print(f"WITHOUT EMAIL BUTTON ERROR \n{e}")
            return None

        try:

            driver.implicitly_wait(20)
            choose_network_for_tether_trc20 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[3]/div/div/label[4]')
            driver.execute_script("arguments[0].click();", choose_network_for_tether_trc20)

            driver.implicitly_wait(10)
            continue_choose_network = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[4]/div/div[2]/div/button')
            driver.execute_script("arguments[0].click();", continue_choose_network)
            sleep(3)

        except Exception as e:
            print(f"CHOOSE NETWORK ERROR \n{e}")
            return None

    except Exception as e:
        print(f"CHOOSE TETHER TRC20 ERROR \n{e}")
        return None

    try:
        driver.set_window_size(1000, 700)
        sleep(2)

        amount = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/p'))
        )
        amount = amount.text.replace(" USDT", "")

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
        print(f"DATA ERROR \n{e}")
        return None

def wallet():
    wallet_data = get_wallet()
    return wallet_data

if __name__ == "__main__":
    wallet()