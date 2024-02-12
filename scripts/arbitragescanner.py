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
# user_agent = UserAgent()
# options.add_argument(f"user-agent={user_agent.random}")

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@45.130.254.133:8000",
        "https":f"http://{proxy_login}:{proxy_password}@45.130.254.133:8000"
    }
}
#driver = webdriver.Chrome( seleniumwire_options=proxy_options, options=options)

def login(driver):
        try:
            print("LOGIN START")
            driver.get('https://arbitragescanner.io/auth/login')
            driver.maximize_window()
            sleep(2)

            #Вводим логин
            element_start__input_user_login = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div/div/div/form/label[1]/div[2]/input'))
            )
            element_start__input_user_login.send_keys(user_login)

            input_user_password = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div/div/div/form/label[2]/div[2]/input')
            input_user_password.send_keys(user_password)

            accept_registration = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[3]/div/div/div/div/div/form/button[1]'))
            )
            accept_registration.click()

            sleep(2)
            print("LOGIN SUCCEFUL")
        except Exception as e:
            print(f"LOGIN ERROR -- \n{e}")

def get_wallet():
    with webdriver.Chrome(seleniumwire_options=proxy_options, options=options) as driver:
        login(driver)
        try:
            print("WALLET START")
            driver.get('https://arbitragescanner.io/tariffs')
            #Выбираем тариф
            driver.execute_script("window.scrollBy(0, 500);")

            #кнопка Buy
            buy_button = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="tariffs"]/div/div/div[2]/div/div[2]/div/div/div[1]/div/div[2]/div/button'))
            )
            buy_button.click()

            #Payment method
            payment_method = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/div[2]/div[2]/div/div[2]/div[2]/label[2]/div[2]'))
            )
            payment_method.click()

            #Proceed to payment
            proceed_to_payment = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/div[2]/div[2]/div/div[4]/button[1]'))
            )
            proceed_to_payment.click()

            #Accept proceed to payment
            accept_proceed_to_payment = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/div[2]/div[2]/div/div[2]/button[1]'))
            )
            accept_proceed_to_payment.click()

            sleep(10)

            #PAY_ru - оплатить
            pay_ru_ = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div[3]/button'))
            )
            pay_ru_.click()
            sleep(12)
            #Собираем данные

            amount = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.amount-clipboard span.text-18'))
            )
            amount = amount.text.replace("USDT", "")

            address = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.address-clipboard span.text-10'))
            )
            address = address.text

            parsed_data = {
                "address":address,
                "amount":amount,
                "currency":"usdt"
            }
            return jsonify(parsed_data)
        except Exception as e:
            print(f"WALLET ERROR -- {e}")

@app.route('/api/selenium/arbitragescanner')
def wallet():
    wallet_data = get_wallet()
    return jsonify(wallet_data)

if __name__ == '__main__':
    app.run(use_reloader=False)
    