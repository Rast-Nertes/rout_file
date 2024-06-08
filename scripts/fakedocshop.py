from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://fakedocshop.com/memberships/'
user_login = "nobrandnametoshow@gmail.com"
user_password = "PPZKQ6rqhS!6yW"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        actions = ActionChains(driver)
        driver.get("https://fakedocshop.com/login/")
        driver.maximize_window()

        try:
            driver.implicitly_wait(10)
            input_log = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/form/div[1]/div/div[1]/div[2]/input')
            input_log.clear()
            input_log.send_keys("Kira")

            driver.implicitly_wait(10)
            input_password = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/form/div[1]/div/div[2]/div[2]/input')
            input_password.clear()
            input_password.send_keys("2233445566")

            driver.implicitly_wait(10)
            submit_button = driver.find_element(By.ID, 'um-submit-btn')
            sleep(2)
            driver.execute_script("arguments[0].click();", submit_button)
            sleep(7.5)
        except Exception as e:
            return {"status": "0", "ext": f"error submit {e}"}

        driver.get(url)

        try:
            driver.implicitly_wait(10)
            choose_tariff = driver.find_element(By.XPATH, '(//button[@type="button"])[1]')
            sleep(5)
            choose_tariff.click()
        except Exception as e:
            return {"status":"0", "ext":f"error choose tariff {e}"}

        try:
            driver.implicitly_wait(10)
            choose_currency = driver.find_element(By.ID, 'mcc_currency_id')
            sleep(2)
            choose_currency.click()

            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.5)
            actions.send_keys(Keys.ENTER).perform()
            sleep(0.5)
        except Exception as e:
            return {"status":"0", "ext":f"error currency{e}"}

        try:
            driver.implicitly_wait(10)
            purchase_button = driver.find_element(By.ID, 'edd-purchase-button')
            sleep(2)
            driver.execute_script("arguments[0].click();", purchase_button)
        except Exception as e:
            return {"status":"0", "ext":f"error purchase {e}"}

        try:
            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, 'div.section > div > div > div.mcc.online_payment_instructions.mycryptocheckout > div > p > span.amount > span > input').get_attribute('value').replace('USDT', '').replace(" ", '')

            driver.implicitly_wait(20)
            address = driver.find_element(By.CSS_SELECTOR, 'div.section > div > div > div.mcc.online_payment_instructions.mycryptocheckout > div > p > span.to > span > input').get_attribute('value')

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
