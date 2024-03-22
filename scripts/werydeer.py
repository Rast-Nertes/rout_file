import urllib.parse
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

url = 'https://wery.deer.su/payitem/16'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"

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
        payok_button = driver.find_element(By.XPATH, '//*[@id="methods"]/div[3]')
        sleep(4)
        driver.execute_script("arguments[0].click();", payok_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.CSS_SELECTOR, 'div.staticModalMiniBlock > div > div:nth-child(3) > input[type=text]')
        input_email.clear()
        input_email.send_keys(user_email)
    except Exception as e:
        print(f"ERROR INPUT EMAIL \n{e}")

    try:
        driver.implicitly_wait(20)
        complete_payment = driver.find_element(By.ID, 'completePayment')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", complete_payment)
    except Exception as e:
        print(f'ERROR COMPLETE PAYMENT \n{e}')

    try:
        driver.implicitly_wait(40)
        choose_trc20 = driver.find_element(By.ID, 'pay_tether_trc_button_open')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", choose_trc20)

        driver.implicitly_wait(30)
        submit_button = driver.find_element(By.ID, 'pay_tether_trc_generate_button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", submit_button)
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(5)
            src_element = driver.find_element(By.XPATH, '/html/body/main/div[1]/div[3]/div[7]/div[2]/div[4]/div/div[2]/img')
            src = src_element.get_attribute('src')

            parsed_url = urllib.parse.urlparse(src)
            query_params = urllib.parse.parse_qs(parsed_url.query)

            address = query_params['chl'][0].split(':')[1].split('?')[0]
            amount = query_params['chl'][0].split('=')[1]

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
