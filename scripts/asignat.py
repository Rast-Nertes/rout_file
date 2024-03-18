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

url = 'https://asignat.com/ru/signIn'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

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


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.CSS_SELECTOR, 'div > form.form.login_step1 > label:nth-child(1) > input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'div > form.form.login_step1 > label:nth-child(2) > input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'div > form.form.login_step1 > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    sleep(2)
    driver.get('https://asignat.com/account/wallet')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(10)
            append_amount = driver.find_element(By.CSS_SELECTOR, 'div.personal__main > section > div.table > div:nth-child(2) > div.r > div:nth-child(1) > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", append_amount)

            driver.implicitly_wait(10)
            select = driver.find_element(By.XPATH, '/html/body/main/div/div[2]/section/div[1]/div[3]/div/form/div[1]/div/label/div')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", select)

            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div[19]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            next_step_button = driver.find_element(By.CSS_SELECTOR, 'div.action.action_repl_usd.showed > div > form > div:nth-child(3) > div > label > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step_button)
        except Exception as e:
            print(f"NEXT STEP BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR, 'div.action.action_repl_usd.showed > div > div.repl_submit_result > form > div:nth-child(2) > div > label > input[type=text]').get_attribute('value')

            driver.implicitly_wait(10)
            amount_text = driver.find_element(By.CSS_SELECTOR, 'div.action.action_repl_usd.showed > div > div.repl_submit_result > form > div:nth-child(1) > div').text
            position_usdt = amount_text.find("USDT")
            amount = amount_text[:position_usdt].replace("Совершите перевод", "").replace(" ", '')

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
