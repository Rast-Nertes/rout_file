from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://dobreplastiki.com/en/albanian-dl/driver-license-albanian'
site_key = '6Lc9h3oUAAAAAIVlZ8EWCx1ycpVDxAS8WKYV0mYO'
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


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    driver.execute_script("arguments[0].click();", elem_click)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        input_data(driver, 30, '/html/body/section/div[2]/div[2]/form/div[1]/div/div/input', '123123123')
        input_data(driver, 30, '/html/body/section/div[2]/div[2]/form/div[2]/div/div/input', '123123123')
        input_data(driver, 30, '/html/body/section/div[2]/div[2]/form/div[3]/div/div/input', '123123123')
        input_data(driver, 30, '/html/body/section/div[2]/div[2]/form/div[4]/div/div/input', '123123123')
        input_data(driver, 30, '/html/body/section/div[2]/div[2]/form/div[5]/div/div/input', '123123123')
        input_data(driver, 30, '/html/body/section/div[2]/div[2]/form/div[6]/div/div/input', '123123123')
        input_data(driver, 30, '/html/body/section/div[2]/div[2]/form/div[7]/div/div/input', '123123123')
        input_data(driver, 30, '/html/body/section/div[2]/div[2]/form/div[8]/div/div/input', '123123123')
        input_data(driver, 30, '/html/body/section/div[2]/div[2]/form/div[9]/div/div/input', '123123123')
    except Exception as e:
        print(f'error input \n{e}')

    try:
        driver.implicitly_wait(20)
        delete_type = driver.find_element(By.XPATH, '/html/body/section/div[2]/div[2]/form/div[10]/div/div/input')
        driver.execute_script("arguments[0].removeAttribute('type');", delete_type)

        driver.implicitly_wait(20)
        delete_type = driver.find_element(By.XPATH, '/html/body/section/div[2]/div[2]/form/div[11]/div/div/input')
        driver.execute_script("arguments[0].removeAttribute('type');", delete_type)
    except Exception as e:
        print(f'error delete type \n{e}')

    try:
        input_data(driver, 30, '/html/body/section/div[2]/div[2]/form/div[10]/div/div/input', '123123123')
        input_data(driver, 30, '/html/body/section/div[2]/div[2]/form/div[11]/div/div/input', '123123123')
    except Exception as e:
        print(f'error input data 2')

    try:
        click(driver, 20, '/html/body/section/div[2]/div[2]/form/div[13]/div/button')
        sleep(1)
        click(driver, 20, '/html/body/section/div/div/div[2]/a')
        sleep(1)
        click(driver, 20, '/html/body/form/section/div/div[2]/div[2]/button')
    except Exception as e:
        print(f"ERROR ADD \n{e}")

    try:
        input_data(driver, 20, '/html/body/section/div/div[1]/div[2]/form/div[1]/div[1]/div/input', "123123123")
        input_data(driver, 20, '/html/body/section/div/div[1]/div[2]/form/div[1]/div[2]/div/input', user_email)
        input_data(driver, 20, '/html/body/section/div/div[1]/div[2]/form/div[1]/div[3]/div/div/input', "123123123")
        input_data(driver, 20, '/html/body/section/div/div[1]/div[2]/form/div[2]/div[1]/div/input', "123123123")
        input_data(driver, 20, '/html/body/section/div/div[1]/div[2]/form/div[2]/div[2]/div/input', "123123123")
        input_data(driver, 20, '/html/body/section/div/div[1]/div[2]/form/div[2]/div[3]/div/input', "123123123")
    except Exception as e:
        print(f'error input data 3 \n{e}')

    try:
        click(driver, 20, '//*[@id="payment_bitcoin"]')
        click(driver, 20, '//*[@id="shipping_courier"]')
        sleep(1)
        click(driver, 20, '/html/body/section/div/div[2]/div[2]/button')
    except Exception as e:
        print(f"Error choose wallet \n{e}")

    try:
        click(driver, 20, '/html/body/section/div/div[2]/div/div/button[4]')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '/html/body/section/div/div[2]/div[2]/ul/li[2]').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '/html/body/section/div/div[2]/div[2]/ul/li[1]').text

            return {
                "address": address,
                "amount": amount.replace('USDTTRC20', '').replace(' ', ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
