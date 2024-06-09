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

url = 'https://psd-seller.com/downloads/poland-id-card-template-psd/'
user_login = "kiracase34@gmail.com"
user_password = "kiramira555"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        driver.get('https://psd-seller.com/downloads/luxembourg-id-card-template-psd/')
        driver.maximize_window()

        try:
            driver.implicitly_wait(10)
            purchase_button = driver.find_element(By.XPATH, '//*[@id="edd_purchase_169-3"]/div/button')
            sleep(3)
            purchase_button.click()
        except Exception as e:
            print(f"PURCHASE ERROR \n{e}")

        try:
            driver.implicitly_wait(30)
            checkout_button = driver.find_element(By.XPATH, '//*[@id="edd_purchase_169-3"]/div/a')
            sleep(3)
            checkout_button.click()
        except Exception as e:
            print(f"CHECKOUT BUTTON ERROR \n{e}")

        sleep(5)

        try:
            driver.implicitly_wait(10)
            cart_empty_find = driver.find_element(By.ID, 'edd_checkout_wrap').text
            if "empty" in cart_empty_find:
                driver.get('https://psd-seller.com/downloads/luxembourg-id-card-template-psd/')

                try:
                    driver.implicitly_wait(10)
                    purchase_button = driver.find_element(By.XPATH, '//*[@id="edd_purchase_169-3"]/div/button')
                    sleep(3)
                    purchase_button.click()
                except Exception as e:
                    print(f"PURCHASE ERROR \n{e}")

                try:
                    driver.implicitly_wait(30)
                    checkout_button = driver.find_element(By.XPATH, '//*[@id="edd_purchase_169-3"]/div/a')
                    sleep(5)
                    checkout_button.click()
                except Exception as e:
                    print(f"CHECKOUT BUTTON ERROR \n{e}")

        except Exception as e:
            print(f"ITEM`s HERE.")
        
        sleep(2)
        
        try:
            driver.implicitly_wait(30)
            input_email = driver.find_element(By.ID, 'edd-email')
            input_email.clear()
            input_email.send_keys(user_login)

            driver.implicitly_wait(10)
            input_first_name = driver.find_element(By.ID, 'edd-first')
            input_first_name.clear()
            input_first_name.send_keys("Kira")

            driver.implicitly_wait(10)
            input_last_name = driver.find_element(By.ID, 'edd-last')
            input_last_name.clear()
            input_last_name.send_keys("Ivanova")
        except Exception as e:
            print(f"INPUT DATA ERROR \n{e}")

        try:
            click_ticket = driver.find_element(By.XPATH, '//*[@id="edd-agree-to-privacy-policy"]')
            sleep(1.5)
            click_ticket.click()
        except Exception as e:
            print(f'ERROR TICKET \n{e}')

        try:
            driver.implicitly_wait(10)
            purchase_button_2 = driver.find_element(By.ID, 'edd-purchase-button')
            sleep(3)
            driver.execute_script("arguments[0].click();", purchase_button_2)
        except Exception as e:
            print(f"PURCHASE BUTTON2 ERROR")

        try:
            driver.implicitly_wait(10)
            choose_tether = driver.find_element(By.CSS_SELECTOR, 'bp-public-invoice-card > div > div > div > bp-public-invoice-card-state-prepared > div > div:nth-child(2) > a > button')
            sleep(2)
            driver.execute_script("arguments[0].click();", choose_tether)
        except Exception as e:
            print(f"CHOOSE TETHER ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, 'div.active-state__main-container > div.active-state__component-main-text > span.active-state__send.ng-star-inserted > span:nth-child(1)').text.replace(" ", "")


            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR, 'bp-public-invoice-card > div > div > div > div.active-state__main-container > div.active-state__component-main-text > div > p').text

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
