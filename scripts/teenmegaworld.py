from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS
#form_token_login
url = 'https://vrbangers.com/join-now/'
user_email = "rwork875@gmail.com"
user_password = "rwork129"

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

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        agree_button = driver.find_element(By.ID, 'agree')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", agree_button)
    except:
        pass

    try:
        driver.implicitly_wait(20)
        choose_crypto = driver.find_element(By.XPATH, '//*[@id="join-now-component"]/div/div[1]/div[1]/div/div[2]/div/button[2]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", choose_crypto)
        sleep(2)

        driver.implicitly_wait(20)
        choose_method = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div[1]/div/div[3]/div[3]/div/div[4]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", choose_method)
    except Exception as e:
        print(f"ERROR CHOOSE METHOD \n{e}")

    try:
        driver.implicitly_wait(20)
        change = driver.find_element(By.XPATH, '//*[@id="single-tarif"]/div/div/div[2]/div[1]/div/div[3]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", change)

        driver.implicitly_wait(10)
        choose = driver.find_element(By.XPATH, '//*[@id="join-now-component"]/div/div[1]/div[1]/div/div[3]/div[2]/div/div[4]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", choose)
    except Exception as e:
        print(f"ERROR CHANGE \n{e}")

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.ID, 'email')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '//*[@id="password"]')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.ID, 'hit-to-join')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(60)
            choose_trc20 = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div[3]/div[2]/div/div[6]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"ERROR CHOOSE TRC20 \n{e}")

        try:
            driver.implicitly_wait(30)
            address = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div[1]').text

            driver.implicitly_wait(10)
            amount = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[3]').text

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
