import requests
from selenium import webdriver
from time import sleep
from flask import Flask, jsonify
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#

#CONSTANS
app = Flask(__name__)
user_login = 'kiracase34@gmail.com'
user_password = 'Kirakira123'
url = 'https://accounts.mobidea.com/idp/login'

#API CONSTANS
API_KEY = '7f728c25edca4f4d0e14512d756d6868'
API_URL = 'http://rucaptcha.com/in.php'
API_RESULT_URL = f'http://rucaptcha.com/res.php?key={API_KEY}&action=get'

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

#   driver = webdriver.Chrome(options= options)

def login(driver):
    driver.get(url)
    driver.maximize_window()
    try:
        input_email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="form"]/div[1]/input'))
        )
        input_email.send_keys(user_login)

        input_password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]'))
        )
        input_password.send_keys(user_password)

        button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="form"]/div[4]/input'))
        )
        sleep(3)
        button.click()
    except Exception as e:
        print(f"INPUT ERROR \n{e}")

def get_wallet():
    with webdriver.Chrome(options) as driver:
        login(driver)
        actions = ActionChains(driver)
        driver.get('https://affiliates.mobidea.com')

        try:
            go_to_cash = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="root_menu"]/div/div[2]/div[1]/div[2]/div/div/div/div[2]/div[1]/a'))
            )
            go_to_cash.click()

            go_to_cash_step_2 = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="top"]/div[2]/div[3]/div/div[3]/div[1]/div[1]/ul/li[4]/a')))
            go_to_cash_step_2.click()

        except Exception as e:
            print(f"ERROR PATH GO CASH \n{e}")

        try:
            try:
                sleep(5)
                actions.send_keys(Keys.ESCAPE).perform()
            except:
                print("Close err")

            input = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="topup_amount"]'))
            )
            input.clear()
            input.send_keys('52')

            choose_wallet = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="topup-form"]/div[1]/div/div[1]/div[3]/div/div/div[3]/a'))
            )
            choose_wallet.click()

            choose_trc20 = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="js-topup-24"]'))
            )
            choose_trc20.click()

            try:
                deposit_money = WebDriverWait(driver,  10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="topup-form"]/div[1]/div/div[1]/div[6]/div/div/button'))
                )
                deposit_money.click()

                deposit_next_step = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div/div[3]/div[2]/div[5]/div/div[1]/div[1]/div[1]/a'))
                )
                deposit_next_step.click()
            except Exception as e:
                print(f"DEPOSIT ERROR \n{e}")

        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")

        sleep(5)
        driver.execute_script("window.scrollBy(0, 100);")
        all_tabs = driver.window_handles
        # Переключаемся на последнюю (новую) вкладку
        new_tab = all_tabs[-1]
        driver.switch_to.window(new_tab)

        amount = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="ammount-copy"]'))
        )
        amount = amount.text

        address = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="payment_conform"]/div[2]/div[2]/div[1]/div/input'))
        )
        address = address.get_attribute('value')

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }

@app.route('/api/selenium/mobidea')
def wallet():
    wallet_data = get_wallet()
    #print(wallet_data)
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5029)