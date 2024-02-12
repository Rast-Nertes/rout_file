import cloudscraper
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

#Triple a

#CONSTANS
app = Flask(__name__)
scrap = cloudscraper.create_scraper()
user_login = 'kiracase34@gmail.com'
user_password = 'kirakira123'
url = 'https://www.proxy4free.com/login/'

#API CONSTANS
api_key = '7f728c25edca4f4d0e14512d756d6868'

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

#driver = webdriver.Chrome(options= options)

def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        input_email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/form/div[3]/div[2]/div/div/div/input'))
        )
        input_email.send_keys(user_login)

        input_password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/form/div[4]/div[2]/div/div/div/input'))
        )
        input_password.send_keys(user_password)

    except Exception as e:
        print(f"INPUT ERROR\n{e}")

    try:
        button_log_in = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/form/button'))
        )
        button_log_in.click()
    except Exception as e:
        print(f"BUTTON ERROR \n{e}")

def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        sleep(3)
        driver.get('https://www.proxy4free.com/user/pricing/')
        try:
            buy_plan = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="ResidentialProxy"]/div[1]/div[1]/button'))
            )
            buy_plan.click()
        except Exception as e:
            print(f"BUY PLAN ERROR \n{e}")

        try:
            sleep(2)
            driver.execute_script("window.scrollBy(0, 220);")
            confirm_payment = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="pay_main"]/button'))
            )
            confirm_payment.click()
        except Exception as e:
            print(f"CONFIRM ERROR \n{e}")

        sleep(5)
        new_window = driver.window_handles[1]
        driver.switch_to.window(new_window)

        choose_usdt = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/triplea-ecommerce-payment-v1/main/section/div/div/div/div/span/div/div[2]/div[2]/div/div[6]/div/div'))
        )
        choose_usdt.click()

        accept_usdt_20 = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="crypto-option-list"]/div/div[3]/div'))
        )
        accept_usdt_20.click()

        try:
            input_name = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="triplea-home"]/div/div/div/div/span/div/fieldset/div/input'))
            )
            input_name.send_keys(user_login)

            accept_name = WebDriverWait(driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="terms-and-conditions"]'))
            )
            accept_name.click()

            button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="triplea-home"]/div/div/div/div/span/div/div[4]/button'))
            )
            button.click()
        except Exception as e:
            print(f"NAME ERROR \n{e}")

        try:
            sleep(6)
            amount = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="triplea-payment-form"]/div/div[3]/div[2]/div[1]/span[1]'))
            )
            amount = amount.text
            print(amount)

            address = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="triplea-payment-form"]/form/div[1]/div/div/div[1]'))
            )
            address = address.text
            print(address)
            return {
                "address":address,
                "amount":amount,
                "currency":"usdt"
            }
        except Exception as e:
            print(f"INFO ERROR \n{e}")
            return None

@app.route('/api/selenium/proxy4free')
def wallet():
    wallet_data = get_wallet()
    #print(wallet_data)
    return jsonify(wallet_data)


if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5027)
    #wallet()