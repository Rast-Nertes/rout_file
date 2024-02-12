from selenium import webdriver
import pyautogui
from time import sleep
from flask import Flask, jsonify
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Zerocryptopay

#CONSTANS
app = Flask(__name__)
user_login = 'kiracase34@gmail.com'
user_password = 'GGGggg1212'
url = 'https://farmfb.store'

#CHROME CONSTANS
chrome_options = webdriver.ChromeOptions()
user_agent = UserAgent()
chrome_options.add_argument(f"user-agent={user_agent.random}")
chrome_options.add_argument("--disable-save-password-bubble")
chrome_options.add_argument("--auto-accept-alerts")
chrome_options.add_experimental_option("prefs", {
  "profile.default_content_setting_values.notifications": 1
})
#chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

def login():
    actions = ActionChains(driver)
    driver.get("https://sease.it/en-us/products/sease-cap-dark-brown-ac033tn278x65")
    driver.maximize_window()

    pyautogui.moveTo(200, 150)
    try:
        driver.implicitly_wait(5)
        accept_rules = driver.find_element(By.XPATH, '//*[@id="iubenda-cs-banner"]/div/div/div/div[3]/div[2]/button[2]')
        driver.execute_script("arguments[0].click();", accept_rules)

        driver.implicitly_wait(5)
        close_ = driver.find_element(By.XPATH, '//*[@id="newsletter-popup"]/div[1]/svg')
        driver.execute_script("arguments[0].click();", close_)
    except:
        pass

    try:
        driver.implicitly_wait(30)
        add_to_cart = driver.find_element(By.XPATH, '//*[@id="AddToCart--template--19106463252825__16394027014784075b"]')
        driver.execute_script("arguments[0].click();", add_to_cart)

        driver.implicitly_wait(30)
        show_cart = driver.find_element(By.XPATH, '//*[@id="CartContainer"]/form/div[2]/div[2]/button')
        driver.execute_script("arguments[0].click();", show_cart)
    except Exception as e:
        print(f"CART ERROR \n{e}")

    try:
        driver.implicitly_wait(30)
        ticket = driver.find_element(By.XPATH, '//*[@id="cart-form"]/div[3]/div[3]/div[1]/label')
        driver.execute_script("arguments[0].click();", ticket)
    except Exception as e:
        print(f"TICKET ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        continue_step = driver.find_element(By.XPATH, '/html/body/div[5]/main/div/div/div[2]/form/div[4]/button')
        driver.execute_script("arguments[0].click();", continue_step)
    except Exception as e:
        print(f"CONTINUE ERROR \n{e}")

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.XPATH, '//*[@id="email"]')
        input_email.send_keys(user_login)

        driver.implicitly_wait(30)
        input_first_name = driver.find_element(By.XPATH, '//*[@id="TextField7"]')
        input_first_name.send_keys("Rast")

        driver.implicitly_wait(30)
        input_last_name = driver.find_element(By.XPATH, '//*[@id="TextField8"]')
        input_last_name.send_keys("Nertes")
    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        driver.implicitly_wait(30)
        input_address = driver.find_element(By.XPATH, '//*[@id="shipping-address1"]')
        input_address.send_keys("1200")

        try:
            #Animation
            sleep(3)
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.5)
            actions.send_keys(Keys.ENTER).perform()
            sleep(0.5)
        except Exception as e:
            print(f"CHOOSE ERROR")

        try:
            driver.implicitly_wait(30)
            input_number = driver.find_element(By.XPATH, '//*[@id="TextField11"]')
            input_number.send_keys('+1 223-333-1331')
        except Exception as e:
            print(f"NUM ERROR \n{e}")
    except Exception as e:
        print(f"ERROR INPUT ADDRESS \n{e}")

    try:
        driver.implicitly_wait(30)
        choose_lunu_crypto_pay = driver.find_element(By.XPATH, '//*[@id="basic"]/div/div[3]/label')
        driver.execute_script("arguments[0].click();", choose_lunu_crypto_pay)
    except Exception as e:
        print(f"CHOOSE LUNU CRYPTO PAY ERROR \n{e}")

    try:
        pay_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="pay-button-container"]/div/div/button'))
        )
        pay_now_button.click()
    except Exception as e:
        print(f"PAY NOW ERROR \n{e}")

    try:
        #На этом моменте трабл
        try:
            driver.implicitly_wait(10)
            src_tag_find = driver.find_element(By.XPATH, '//*[@id="lunu-payment-widget"]/div/iframe')
            src = src_tag_find.get_attribute('src')
            driver.get(src)

            driver.implicitly_wait(10)
            choose_wallet = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div[1]/div/div/div/div')
            driver.execute_script("arguments[0].click();", choose_wallet)
        except Exception as e:
            print(f"CHOOSE WALLET ERROR \n{e}")

        try:
            driver.implicitly_wait(30)
            choose_lunu_wallet = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div[2]/div[2]/div/div[42]/div[2]')
            driver.execute_script("arguments[0].click();", choose_lunu_wallet)
        except Exception as e:
            print(f"CHOOSE LUNU WALLET \n{e}")

        driver.implicitly_wait(30)
        next_step = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div[3]/div/a')
        driver.execute_script("arguments[0].click();", next_step)

    except Exception as e:
        print(f"NEXT STEP ERROR \n{e}")

    try:
        driver.implicitly_wait(30)
        choose_usdt = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/div/div[3]/div/div/div[2]')
        driver.execute_script("arguments[0].click();", choose_usdt)

        try:
            driver.implicitly_wait(30)
            choose_trc20 = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/div[2]/div[1]/div[2]')
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")
    except Exception as e:
        print(f"CHOOSE USDT ERROR \n{e}")

    try:
        amount = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/div[1]/div/span[2]'))
        )
        amount = amount.text.replace(" USDT", "")

        driver.implicitly_wait(10)
        address_copy = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[3]/div/div/a')
        driver.execute_script("arguments[0].click();", address_copy)
        sleep(2)

        pyautogui.moveTo(300, 230)
        pyautogui.click()

        sleep(1)
        address = driver.execute_script("return navigator.clipboard.readText();")
        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }
    except Exception as e:
        print(f"DATA ERROR \n{e}")

def wallet():
    get_wallet = login()
    print(get_wallet)
    return get_wallet

if __name__ == "__main__":
    wallet()