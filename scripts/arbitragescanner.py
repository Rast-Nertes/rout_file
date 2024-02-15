from time import sleep
from flask import Flask
from flask import jsonify
#from selenium import webdriver
from fake_useragent import UserAgent
from seleniumwire import webdriver
#import undetected_chromedriver2 as uc2
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#CONSTANS

app = Flask(__name__)
url = 'https://arbitragescanner.io/'
user_login = 'kiracase34@gmail.com'
user_password = 'kiraoleg00'

#PROXY_CONSTANS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

#CHROME OPTIONS

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--disable-save-password-bubble")
options.add_argument('--auto-open-devtools-for-tabs')
# user_agent = UserAgent()
# options.add_argument(f"user-agent={user_agent.random}")

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@45.130.254.133:8000",
        "https":f"http://{proxy_login}:{proxy_password}@45.130.254.133:8000"
    }
}


def login(driver):
    driver.get('https://arbitragescanner.io/auth/login')
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div/div/div/form/label[1]/div[2]/input')
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_pass = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div/div/div/form/label[2]/div[2]/input')
        input_pass.send_keys(user_password)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        button_login = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div/div/div/form/button[1]')
        driver.execute_script("arguments[0].click();", button_login)
        sleep(5)
    except Exception as e:
        print(f"BUTTON LOG IN ERROR \n{e}")



def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)
        try:
            print("WALLET START")
            driver.get('https://arbitragescanner.io/tariffs')

            #Выбираем тариф

            try:
                driver.implicitly_wait(10)
                buy_button = driver.find_element(By.CSS_SELECTOR, '.section-plans-tariff__price_btn button')
                driver.execute_script("arguments[0].click();", buy_button)
            except Exception as e:
                print(f"CHOOSE TARIFF ERROR \n{e}")

            try:
                driver.implicitly_wait(10)
                button_proceed_to_payment = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[4]/div/div[2]/div[2]/div/div[4]/button[1]')
                driver.execute_script("arguments[0].click();", button_proceed_to_payment)
            except Exception as e:
                print(f'PROCEED BUTTON ERROR \n{e}')

            try:
                driver.implicitly_wait(10)
                button_proceed_to_payment = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[4]/div/div[2]/div[2]/div/div[2]/button[1]')
                driver.execute_script("arguments[0].click();", button_proceed_to_payment)
            except Exception as e:
                print(f'PROCEED BUTTON ERROR \n{e}')

            try:
                driver.implicitly_wait(10)
                amount = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div[1]/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div[2]/div[2]/b')
                amount = amount.text.replace(" $", "")
                print(amount)
            except Exception as e:
                print(f"AMOUNT ERROR \n{e}")
                amount = 'None'

            try:
                address = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[4]/div/div[2]/div[2]/div/div[2]/img'))
                )
                address = address.get_attribute('src')
                result_address = address.split("/")[-1].split(".")[0]
                print(result_address)
            except Exception as e:
                print(f"ADDRESS ERROR \n{e}")

            return {
                "address":result_address,
                "amount":amount,
                "currency":"usdt"
            }

        except Exception as e:
            print(f"WALLET ERROR -- {e}")

def wallet():
    wallet_data = get_wallet()
    return jsonify(wallet_data)

    