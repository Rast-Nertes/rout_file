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
        sleep(5)
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.XPATH, '//input[@name="email"]')
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_pass = driver.find_element(By.XPATH, '//input[@name="password"]')
        input_pass.send_keys(user_password)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        button_login = driver.find_element(By.XPATH, '//button[@type="submit"]')
        driver.execute_script("arguments[0].click();", button_login)
        sleep(5)
    except Exception as e:
        print(f"BUTTON LOG IN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)
        try:
            print("WALLET START")
            try:
                driver.implicitly_wait(10)
                click_buy_paln = driver.find_element(By.XPATH, '//div[@class="header-plan"]')
                click_buy_paln.click()
            except Exception as e:
                print(f'ERROR CLICK BUY PLAN \n{e}')
            #Выбираем тариф

            try:
                driver.implicitly_wait(10)
                buy_button = driver.find_element(By.CSS_SELECTOR, '.section-plans-tariff__price_btn button')
                driver.execute_script("arguments[0].click();", buy_button)
            except Exception as e:
                print(f"CHOOSE TARIFF ERROR \n{e}")

            try:
                driver.implicitly_wait(10)
                button_proceed_to_payment = driver.find_element(By.XPATH, '(//button[@type="button"])[13]')
                sleep(1.5)
                button_proceed_to_payment.click()
            except Exception as e:
                print(f'PROCEED BUTTON ERROR \n{e}')

            try:
                driver.implicitly_wait(10)
                amount = driver.find_element(By.XPATH, '(//div[@class="section-plans-tariff__price_price"]/b)[1]')
                amount = amount.text.replace(" $", "")
                # print(amount)
            except Exception as e:
                print(f"AMOUNT ERROR \n{e}")
                amount = 'None'

            try:
                sleep(5)
                address = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '(//img[@src])[3]'))
                )
                address = address.get_attribute('src')
                # print(address)
                # input("press")
                result_address = address.split(".io/")[1].replace("undefined", '').replace(".png", '')
                # print(result_address)
            except Exception as e:
                print(f"ADDRESS ERROR \n{e}")

            return {
                "address":result_address,
                "amount":amount,
                "currency":"usdt"
            }

        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
