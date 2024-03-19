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

url = 'https://cheatrise.com/games/eft/spoofer'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.add_experimental_option("detach", True)


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        driver.maximize_window()
        driver.get(url)

        try:
            driver.implicitly_wait(40)
            buy_button = driver.find_element(By.CSS_SELECTOR, 'div.list.row > div.prices-block.col-md-4 > div > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_button)
        except Exception as e:
            print(f"ERROR BUY BUTTON \n{e}")

        try:
            driver.implicitly_wait(10)
            input_email = driver.find_element(By.ID, 'purchases-email')
            input_email.clear()
            input_email.send_keys(user_email)

            driver.implicitly_wait(10)
            choose_freekassa = driver.find_element(By.CSS_SELECTOR, 'div.pay-sellix.linear-gradient-border.purple')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_freekassa)
        except Exception as e:
            print(f"ERROR CHOOSE PAYMENT \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_tether = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[2]/div[1]/div[3]/div[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_tether)

            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.XPATH, '//*[@id="gateway-body"]/div[2]/div[1]/div[3]/div[2]/div[2]/div[3]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(10)
            submit_payment = driver.find_element(By.XPATH, '//*[@id="gateway-footer"]/div/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit_payment)
        except Exception as e:
            print(f"ERROR CHOOSE TRC20 \n{e}")

        try:
            driver.implicitly_wait(10)
            show_details_button = driver.find_element(By.XPATH, '//*[@id="embed-body"]/div/div[1]/div[6]/div[2]/div[1]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", show_details_button)
        except Exception as e:
            print(f"SHOW DETAILS ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[6]/div[2]/div[2]/div/div[2]/span[2]/div/div[2]/span').text

            driver.implicitly_wait(10)
            amount = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[6]/div[2]/div[2]/div/div[2]/span[1]/div/div[2]/span').text

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
