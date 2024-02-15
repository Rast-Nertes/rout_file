import requests
from seleniumwire import webdriver
from time import sleep
from flask import Flask, jsonify
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

#Aurpay

#CONSTANS

app = Flask(__name__)
url = 'https://www.musicianmadness.com/accessories/korg-metronome-tuner-with-contact-microphone-tm60whtc/'
user_login = 'kiracase34@gmail.com'

#API CONSTANS

API_KEY = '7f728c25edca4f4d0e14512d756d6868'
API_URL = 'http://rucaptcha.com/in.php'
API_RESULT_URL = f'http://rucaptcha.com/res.php?key={API_KEY}&action=get'

#CHROME OPTIONS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.headless = False
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.add_experimental_option("detach", True)

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

#driver = webdriver.Chrome(options=options, seleniumwire_options=proxy_options)

def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        driver.get(url)
        driver.maximize_window()
        actions = ActionChains(driver)

        #Слипы лучше не трогать, клики не успевают обрабатываться

        try:
            driver.implicitly_wait(20)
            add_to_cart_button = driver.find_element(By.XPATH, '//*[@id="form-action-addToCart"]')
            driver.execute_script("arguments[0].click();", add_to_cart_button)
        except Exception as e:
            print(f"ADD TO CART ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            proceed_to_checkout = driver.find_element(By.XPATH, '//*[@id="previewModal"]/div[1]/div[2]/div/section[1]/a[1]')
            driver.execute_script("arguments[0].click();", proceed_to_checkout)
        except Exception as e:
            print(f"PROCEED BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(30)
            input_email = driver.find_element(By.XPATH, '//*[@id="email"]')
            input_email.send_keys(user_login)

            continue_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="checkout-customer-continue"]'))
            )
            continue_button.click()
        except Exception as e:
            print(f"INPUT EMAIL ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            input_first_name = driver.find_element(By.XPATH, '//*[@id="firstNameInput"]')
            input_first_name.send_keys("Kira")

            sleep(1)
            driver.implicitly_wait(20)
            input_second_name = driver.find_element(By.XPATH, '//*[@id="lastNameInput"]')
            input_second_name.send_keys("Ivanova")

        except Exception as e:
            print(f"INPUT NAMES ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            input_address_line_1 = driver.find_element(By.XPATH, '//*[@id="addressLine1Input"]')
            input_address_line_1.send_keys("11111111")

            driver.implicitly_wait(20)
            input_address_line_2 = driver.find_element(By.XPATH, '//*[@id="addressLine2Input"]')
            input_address_line_2.send_keys("11111111")
        except Exception as e:
            print(f"INPUT ADDRESS LINES ERROR \n{e}")

        try:
            sleep(2)
            driver.implicitly_wait(20)
            input_company_name = driver.find_element(By.XPATH, '//*[@id="companyInput"]')
            input_company_name.send_keys("Company")

            driver.implicitly_wait(10)
            input_city = driver.find_element(By.XPATH, '//*[@id="cityInput"]')
            input_city.send_keys("City")

            driver.implicitly_wait(10)
            input_postal_code = driver.find_element(By.XPATH, '//*[@id="postCodeInput"]')
            input_postal_code.send_keys("11111111")

            driver.implicitly_wait(10)
            input_phone_number = driver.find_element(By.XPATH, '//*[@id="phoneInput"]')
            input_phone_number.send_keys("+11111222222")

        except Exception as e:
            print(f"DATA ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            shipping_method_choose = driver.find_element(By.XPATH, '//*[@id="checkout-shipping-options"]/div/div/div/ul/li[1]/div/div/label')
            driver.execute_script("arguments[0].click();", shipping_method_choose)
        except Exception as e:
            print(f"SHIPPING METHOD ERROR \n{e}")

        try:
            # sleep(2)
            # driver.implicitly_wait(20)
            continue_button_step_2 = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="checkout-shipping-continue"]'))
            )
            continue_button_step_2.click()
        except Exception as e:
            print(f"CONTINUE BUTTON STEP2 ERROR \n{e}")

        try:
            sleep(5)
            driver.implicitly_wait(20)
            choose_aurpay = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/div/div/ol/li[4]/div[2]/form/label')
            driver.execute_script("arguments[0].click();", choose_aurpay)
        except Exception as e:
            print(f"CHOOSE AURPAY ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            choose_usdt_trc20 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/section/div/div[3]/div[2]/div[9]')
            driver.execute_script("arguments[0].click();", choose_usdt_trc20)

        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")

        try:
            amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="app"]/div/div/div/div/div[4]/div[2]/div/div/div[1]'))
            )
            amount = amount.text.replace(" USDT TRC20", "")

            address = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="app"]/div/div/div/div/div[4]/div[4]/div/div'))
            )
            address = address.text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")

def wallet():
    wallet_data = get_wallet()
    #print(wallet_data)
    return jsonify(wallet_data)
