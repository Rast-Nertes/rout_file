import pyautogui
#from selenium import webdriver
from time import sleep
from flask import Flask, jsonify
from seleniumwire import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

#Lunu

#CONSTANS

app = Flask(__name__)
url = 'https://sease.it/en-gb/collections/polo-e-t-shirt/products/lampuga-off-white-lr033tj137y38'
user_login = 'kiracase34@gmail.com'
user_password = 'oleg123567'

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

#CHROME OPTIONS

options = webdriver.ChromeOptions()
options.add_argument('--auto-open-devtools-for-tabs')

def path_to_lunu_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        actions = ActionChains(driver)
        driver.get(url)
        driver.maximize_window()

        try:
            driver.implicitly_wait(10)
            add_to_cart_button = driver.find_element(By.XPATH, '//*[@id="AddToCart--template--19106463252825__16394027014784075b"]')
            driver.execute_script("arguments[0].click();", add_to_cart_button)

            driver.implicitly_wait(10)
            show_cart_button = driver.find_element(By.XPATH, '//*[@id="CartContainer"]/form/div[2]/div[2]/button')
            driver.execute_script("arguments[0].click();", show_cart_button)
        except Exception as e:
            print(f'ADD TO CART ERROR \n{e}')

        try:
            driver.implicitly_wait(10)
            ticket = driver.find_element(By.XPATH, '//*[@id="cart-form"]/div[3]/div[3]/div[1]/label')
            driver.execute_script("arguments[0].click();", ticket)

            driver.implicitly_wait(10)
            continue_button = driver.find_element(By.XPATH, '//*[@id="cart-form"]/div[4]/button')
            driver.execute_script("arguments[0].click();", continue_button)
        except Exception as e:
            print(f"ERROR CONTINUE \n{e}")

        try:
            input_phone = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '#TextField5'))
            )
            input_phone.clear()
            input_phone.send_keys('+1 223-322-2111')
        except Exception as e:
            print(f"INPUT PHONE ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_email = driver.find_element(By.XPATH, '//*[@id="email"]')
            input_email.clear()
            input_email.send_keys(user_login)

            driver.implicitly_wait(10)
            input_first_name = driver.find_element(By.XPATH, '//*[@id="TextField0"]')
            input_first_name.send_keys("Kira")

            driver.implicitly_wait(10)
            input_last_name = driver.find_element(By.XPATH, '//*[@id="TextField1"]')
            input_last_name.send_keys("Ivanova")
        except Exception as e:
            print(f"INPUT EMAIL ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_address = driver.find_element(By.XPATH, '//*[@id="shipping-address1"]')
            input_address.clear()
            input_address.send_keys("112")

            sleep(7)
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(1)
            actions.send_keys(Keys.ENTER).perform()

        except Exception as e:
            print(f"ADDRESS ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            choose_lunu_crypto_pay = driver.find_element(By.XPATH, '//*[@id="basic"]/div/div[3]/label')
            driver.execute_script("arguments[0].click();", choose_lunu_crypto_pay)

            sleep(3)
            pay_now = driver.find_element(By.XPATH, '//*[@id="pay-button-container"]/div/div/button')
            driver.execute_script("arguments[0].click();", pay_now)
        except Exception as e:
            print(f"CHOOSE LUNU CRYPTO PAY ERROR \n{e}")

        try:
            driver.implicitly_wait(30)
            iframe_url = driver.find_element(By.XPATH, '//*[@id="lunu-payment-widget"]/div/iframe').get_attribute('src')
            driver.get(iframe_url)
        except Exception as e:
            print(f"IFRAME ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_wallet = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div[1]/div/div/div/div')
            driver.execute_script("arguments[0].click();", choose_wallet)

        except Exception as e:
            print(f'CHOOSE WALLET BUTTON ERROR \n{e}')

        try:
            driver.implicitly_wait(10)
            choose_lunu = driver.find_element(By.CSS_SELECTOR, 'div.h100\%-52.hUnset\.disableHeight.ov.rlv > div > div:nth-child(41) > div.MuiButtonBase-root.dB\*2.abs\*2.s.cr\@mouse')
            driver.execute_script("arguments[0].click();", choose_lunu)

            driver.implicitly_wait(10)
            next_step = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div[3]/div/a')
            driver.execute_script("arguments[0].click();", next_step)
        except Exception as e:
            print(f"CHOOSE LUNU ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_tether = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/div/div[3]/div/div/div[2]')
            driver.execute_script("arguments[0].click();", choose_tether)

            sleep(3)
            trc20_network = driver.find_element(By.CSS_SELECTOR, 'div.pt30 > div:nth-child(1) > div.MuiButtonBase-root.dB\*2.abs\*2.s.cr\@mouse')
            driver.execute_script("arguments[0].click();", trc20_network)
        except Exception as e:
            print(f"CHOOSE TRC20 NETWORK \n{e}")

        try:
            amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/div[1]/div/span[2]'))
            )
            amount = amount.text.replace(" USDT", '')

            sleep(4)
            copy_address = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/div/div/a')
            copy_address.click()

            try:
                driver.execute_script("return navigator.clipboard.readText()")
            except:
                pass

            try:
                sleep(2)
                pyautogui.moveTo(300, 225)
                pyautogui.click()

                address = driver.execute_script("return navigator.clipboard.readText()")
            except Exception as e:
                print(f"ERROR MOVE \n{e}")

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")

def wallet():
    wallet_data = path_to_lunu_wallet()
    #print(wallet_data)
    return jsonify(wallet_data)
