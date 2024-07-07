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

url = 'https://dino-money.mom'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(80)
        input_email = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/div[1]/form/div[2]/table/tbody/tr[1]/td/input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(40)
        input_password = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/div[1]/form/div[2]/table/tbody/tr[2]/td/input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(40)
        login_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[1]/div[1]/form/div[2]/table/tbody/tr[3]/td/div/input')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")
    sleep(3)
    driver.get('https://dino-money.mom/account/insert')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        #Здесь выбор Payeer

        try:
            driver.implicitly_wait(50)
            input_amoun = driver.find_element(By.CSS_SELECTOR, 'div > center:nth-child(11) > div > form > div:nth-child(4) > input[type=number]')
            sleep(1.5)
            input_amoun.clear()
            input_amoun.send_keys('550')

            driver.implicitly_wait(30)
            submit_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[2]/div/center[2]/div/form/input[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit_button)

            driver.implicitly_wait(70)
            next_step = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div[2]/div/center[2]/form/input[8]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step)
        except Exception as e:
            print(f"ERROR INPUT AMOUNT \n{e}")

        try:
            driver.implicitly_wait(60)
            choose_trc20 = driver.find_element(By.ID, 'currency-15')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(40)
            input_email = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[1]/div/form/div/div[2]/input')
            input_email.clear()
            input_email.send_keys(user_email)
        except Exception as e:
            print(f"INPUT EMAIL \n{e}")

        try:
            driver.implicitly_wait(60)
            submit_payment = driver.find_element(By.ID, 'submit-payment')
            sleep(1.5)
            submit_payment.click()
        except Exception as e:
            print(f"SUBMIT ERROR \n{e}")

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[7]/div[2]').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[5]/span').text

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
