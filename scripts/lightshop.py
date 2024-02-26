import time
import pyautogui
from flask import jsonify
from selenium_driverless.sync import webdriver
from selenium_driverless.types.by import By

#CONSTANS

url = 'https://lightshop.su/'
user_login = 'kiracase34@gmail.com'
user_pass = 'oleg34oleg'

#CHROME OPTIONS
with open('config.txt') as file:
    chrome_path = file.read().strip()

options = webdriver.ChromeOptions()
options.binary_location = chrome_path

def get_wallet():

     with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        driver.refresh()
        driver.maximize_window()

        try:
            choose_product = driver.find_element(By.CSS_SELECTOR, 'div.table-responsive > table > tbody > tr:nth-child(13) > td.text-center > a > i', timeout=20)
            time.sleep(2)
            driver.execute_script("arguments[0].click();", choose_product)
        except Exception as e:
            print(f'CHOOSE PRODUCT ERROR \n{e}')

        try:
            input_email_in_product = driver.find_element(By.CSS_SELECTOR, '#order > table > tbody > tr:nth-child(2) > td:nth-child(2) > input[type=text]', timeout=20)
            time.sleep(2)
            input_email_in_product.write(user_login)
        except Exception as e:
            print(f"INPUT EMAIL ERROR \n{e}")

        try:
            choose_payment_xpath1 = '//*[@id="order"]/table/tbody/tr[4]/td[2]/select/option[1]'
            driver.execute_script(f"document.evaluate('{choose_payment_xpath1}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.remove();")

            time.sleep(3)
            choose_payment_xpath2 = '//*[@id="order"]/table/tbody/tr[4]/td[2]/select/option[1]'
            driver.execute_script(f"document.evaluate('{choose_payment_xpath2}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.remove();")
        except Exception as e:
            print(f"ERROR CHOOSE PAYMENT \n{e}")

        try:
            #Время на удаления объекта
            time.sleep(5)
            start_buy = driver.find_element(By.CSS_SELECTOR, '#order > footer > button', timeout=40)
            time.sleep(2)
            driver.execute_script("arguments[0].click();", start_buy)
        except Exception as e:
            print(f"START BUY BUTTON ERROR \n{e}")
            return "Not work"

        try:
            choose_tether = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/form[2]/div[13]', timeout=40)
            time.sleep(3)
            choose_tether.click()
        except Exception as e:
            print(f"CHOOSE TETHER ERROR \n{e}")
            return "Not work"

        try:
            accept = driver.find_element(By.CSS_SELECTOR, 'div.payment-container > div.popup__bg.active > div > div > input', timeout=30)
            time.sleep(5)
            driver.execute_script("arguments[0].click();", accept)
        except Exception as e:
            print(f"CONTINUE BUTTON ERROR \n{e}")
            return "Not work"


        try:
            amount_element = driver.find_element(By.ID, 'pay_amount', timeout=10)
            amount = amount_element.text

            address_element = driver.find_element(By.ID, 'crypto_address', timeout=10)
            address = address_element.text
        except Exception as e:
            print(f"DATA ERROR \n{e}")
            return "Not work"

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }


def wallet():
    wallet_data = get_wallet()
    return jsonify(wallet_data)
