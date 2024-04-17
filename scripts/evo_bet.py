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

url = 'https://evo-bet.com/?modal=login'
user_email = "kiracase34@gmail.com"
user_password = "Re7ffHRkM@3#6p"

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    api_key = paths[2].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


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
        input_data(driver, 35, '//*[@id="headlessui-dialog-3"]/div/div[2]/div[3]/form/div[1]/div/div[1]/input', user_email)
        input_data(driver, 30, '//*[@id="headlessui-dialog-3"]/div/div[2]/div[3]/form/div[1]/div/div[2]/input', user_password)
        click(driver, 20, '//*[@id="headlessui-dialog-3"]/div/div[2]/div[3]/form/div[2]/button')
    except Exception as e:
        print(f'ERROR INPUT LOGIN DATA \n{e}')

    sleep(2.5)
    driver.get('https://evo-bet.com/account/financials/deposit')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        driver.implicitly_wait(20)
        find_frame = driver.find_element(By.TAG_NAME, 'iframe').get_attribute('src')
        sleep(1.5)
        driver.get(find_frame)

        try:
            try:
                driver.implicitly_wait(15)
                amount = driver.find_element(By.XPATH, '/html/body/div/div/div/div/div[2]/div/a[12]/div/div[2]/div[1]/span[2]').text
                print(amount)
            except:
                amount = '10.00'

            try:
                click(driver, 20, '//*[@id="app"]/div/div/div/div[2]/div/a[12]/div/div[1]/img')
            except Exception as e:
                print(f'ERROR CHOOSE TRC20 \n{e}')

            sleep(2.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/div[2]/div/div/div[1]/strong').text

            return {
                "address": address,
                "amount": amount.replace("\n", '').replace("€", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
