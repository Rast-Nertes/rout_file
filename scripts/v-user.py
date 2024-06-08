from time import sleep
from flask import Flask
from flask import jsonify
#from selenium import webdriver
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains
#import undetected_chromedriver2 as uc2
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#PROXY_CONSTANS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000


#CONSTANS

url = 'https://www.hostwinds.com'
user_login = 'kiracase34@gmail.com'
user_password = 'Hkasd12'

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.headless = False

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@45.130.254.133:8000",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def login(driver):
    try:
        driver.get('https://www.v-user.com/en/user-panel-en/login')
        driver.maximize_window()
        sleep(2)

        element_start__input_user_login = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="modlgn-username-106"]'))
        )
        element_start__input_user_login.send_keys(user_login)

        # Вводим пароль

        input_user_password = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="modlgn-passwd-106"]'))
        )
        input_user_password.send_keys(user_password)

        # Заходим

        accept_registration = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="login-form-106"]/div[2]/div[4]/button'))
        )
        accept_registration.click()

        sleep(5)
    except Exception as e:
        return {"status":"0", "ext":f"error login {e}"}


def get_wallet_data():
    with webdriver.Chrome(options = options) as driver:
        login(driver)
        try:
            print("WALLET DATA START")

            driver.get('https://www.v-user.com/en/buy/player-serial-number-of-virtual-user-software')
            sleep(3.5)

            try:
                close = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="iam-here"]/button[1]/i'))
                )
                close.click()
            except:
                pass

            try:
                #Галочку ставим
                tick = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/span/input'))
                )
                sleep(1.5)
                driver.execute_script("arguments[0].click();", tick)

                sleep(1.5)

                #Выбираем оплату с помощью валют
                tick_wallet = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/div/div[1]/div[1]/label'))
                )
                sleep(1.5)
                driver.execute_script("arguments[0].click();", tick_wallet)

                sleep(1.5)
                #Pay now
                accept = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="ppform"]/div[3]/div[2]/div/div[2]/span'))
                )
                driver.execute_script("arguments[0].click();", accept)
            except Exception as e:
                driver.refresh()
                sleep(2.5)
                # Галочку ставим
                tick = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/span/input'))
                )
                driver.execute_script("arguments[0].click();", tick)

                # Выбираем оплату с помощью валют
                tick_wallet = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH,
                                                      '/html/body/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[3]/div[2]/div/div[1]/div[1]/label'))
                )
                driver.execute_script("arguments[0].click();", tick_wallet)

                # Pay now
                accept = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="ppform"]/div[3]/div[2]/div/div[2]/span'))
                )
                driver.execute_script("arguments[0].click();", accept)

            #Continue
            continue_accept = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="submit-btn"]'))
            )
            sleep(2.5)
            driver.execute_script("arguments[0].click();", continue_accept)

            sleep(3)

            all_tabs = driver.window_handles
            new_tab = all_tabs[-1]
            driver.switch_to.window(new_tab)

            choose_tron = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="select2-currency-container"]'))
            )
            choose_tron.click()

            sleep(3)
            actions = ActionChains(driver)
            for _ in range(10):
                actions.send_keys(Keys.ARROW_DOWN).perform()
                sleep(0.5)

            actions.send_keys(Keys.ENTER).perform()
            sleep(5)

            amount = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="amount"]'))
            )
            amount = amount.get_attribute('value').replace('USDT', '')

            address = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="address"]'))
            )
            address = address.get_attribute('value')

            return{
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }

        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet_data()
    print(wallet_data)
    return jsonify(wallet_data)
