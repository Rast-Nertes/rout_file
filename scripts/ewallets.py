from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


#CONSTANS

url = 'https://ewallets.cc/product/oldubil/'
user_login = "rwork875"
user_password = "TQOAyI%Kj078"

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        actions = ActionChains(driver)
        driver.maximize_window()
        driver.get('https://ewallets.cc/my-account/')

        try:
            driver.implicitly_wait(20)
            input_email = driver.find_element(By.ID, 'username')
            input_email.clear()
            input_email.send_keys(user_login)

            driver.implicitly_wait(20)
            input_password = driver.find_element(By.ID, 'password')
            input_password.clear()
            input_password.send_keys(user_password)
        except Exception as e:
            print(f"INPUT DATA ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            button_login = driver.find_element(By.CSS_SELECTOR, 'div.page-wrapper.my-account.mb > div > div > div.account-container.lightbox-inner > div > form > p:nth-child(3) > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", button_login)
        except Exception as e:
            print(f"BUTTON LOGIN ERROR \n{e}")

        driver.get(url)

        try:
            driver.implicitly_wait(10)
            add_to_busket_button = driver.find_element(By.CSS_SELECTOR, 'div > div.product-info.summary.col-fit.col.entry-summary.product-summary.form-minimal > form > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", add_to_busket_button)
        except Exception as e:
            print(f"ADD TO BUSKET ERROR \n{e}")

        driver.get('https://ewallets.cc/cart/')

        try:
            driver.implicitly_wait(20)
            count = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div[2]/div[1]/form/div/table/tbody/tr[1]/td[5]/div/input[2]')
            count.clear()
            count.send_keys("1")
            sleep(1)
            actions.send_keys(Keys.ENTER).perform()
            sleep(7.5)
        except Exception as e:
            print(f"COUNT INPUT ERROR \n{e}")


        driver.get('https://ewallets.cc/checkout/')

        try:
            driver.implicitly_wait(10)
            input_email = driver.find_element(By.ID, 'billing_email')
            input_email.clear()
            sleep(2)
            input_email.send_keys('rwork875@gmail.com')
        except Exception as e:
            print(f"INPUT EMAIL ERROR \n{e}")

        try:
            driver.implicitly_wait(30)
            choose_crypto_currency = driver.find_element(By.ID, 'select2-payment_cryptapi_coin-container')
            sleep(1.5)
            choose_crypto_currency.click()
            sleep(1)

            for _ in range(20):
                actions.send_keys(Keys.ARROW_UP).perform()
                sleep(0.2)

            for _ in range(12):
                actions.send_keys(Keys.ARROW_DOWN).perform()
                sleep(0.5)

            actions.send_keys(Keys.ENTER).perform()
            sleep(5)
        except Exception as e:
            print(f"CHOOSE CRYPTO ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            place_order = driver.find_element(By.ID, 'place_order')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", place_order)
        except Exception as e:
            print(f"PLACE ORDER BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, 'div.ca_payments_wrapper > div.ca_details_box > div:nth-child(1) > button > span:nth-child(1) > b').text

            driver.implicitly_wait(20)
            address = driver.find_element(By.CSS_SELECTOR, 'div.ca_payments_wrapper > div.ca_details_box > div:nth-child(6) > button > span:nth-child(1)').text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
