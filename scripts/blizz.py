import re
from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://blizz.io/'
user_email = "kiracase34@gmail.com"
user_password = "VCtx9_GHkxn!f9h"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    ext = paths[1].strip()

# options.add_extension(ext)
# options.binary_location = chrome_path
#
# proxy_address = "45.130.254.133"
# proxy_login = 'K0nENe'
# proxy_password = 'uw7RQ3'
# proxy_port = 8000
# #
# # proxy_address = "196.19.121.187"
# # proxy_login = 'WyS1nY'
# # proxy_password = '8suHN9'
# # proxy_port = 8000
#
# proxy_options = {
#     "proxy":{
#         "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
#         "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
#     }
# }


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    elem_click.click()


def js_click(driver, time, XPATH):
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
    actions = ActionChains(driver)
    driver.maximize_window()
    driver.get(url)

    try:
        click(driver, 30, '//a[@class="common_btn_v1 inactive login_btn font_regular"]')
        input_data(driver, 30, '//input[@name="email"]', user_email)
        input_data(driver, 30, '//input[@name="password"]', user_password)
        click(driver, 30, '//button[@class="common_btn_v1 login_btn width_100 with_shadow btn btn-primary"]')
    except Exception as e:
        return {"status": "0", "ext": f"Login error \n{e}"}

    try:
        sleep(3.5)
        click(driver, 30, '//*[@id="root"]/div/div/header/section/div/div/div[3]/div[1]/div/div[2]/a')
    except Exception as e:
        return {"status": "0", "ext": f"DEPOS BUT \n{e}"}


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//*[@id="deposit_address"]')
            address = address_elem.get_attribute('value')

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//div[@class="privacy_text bordered_text"]')
            amount_text = amount_elem.text

            amount = re.search(r'\$(\d+)\.', amount_text)

            if amount:
                amount = amount.group(1)

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
