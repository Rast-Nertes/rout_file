import pyautogui
from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://crypto-games.io/en/home'
user_email = "kiracase34"
user_password = "@Dn6QLwum!VtJ"

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
        js_click(driver, 60, '/html/body/app-root/div/app-root/div/app-casino/div/app-header/div/div/div[3]/button[1]')
        input_data(driver, 30, '//*[@id="username"]', user_email)
        input_data(driver, 30, '//*[@id="password"]', user_password)
        sleep(3.5)
        js_click(driver, 30, '/html/body/div/div[2]/div/cdk-dialog-container/app-sign-in/div/div[2]/form/button')
    except Exception as e:
        return {"status": "0", "ext": f"Login error \n{e}. \nCheck script."}

    try:
        js_click(driver, 30, '/html/body/app-root/div/app-root/div/app-casino/div/app-header/div/div/div[3]/app-wallet-button/button')
    except Exception as e:
        return {"status": "0", "ext": f"Depos but error \n{e}"}

    try:
        js_click(driver, 30, '//*[@id="dropDownButton2"]')
        js_click(driver, 30, '//*[@id="buyCryptoCurrencyDropdown2"]/ul/li[2]')
    except Exception as e:
        return {"status": "0", "ext": f"ERROR CHOOSE TRC20 \n{e} "}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/cdk-dialog-container/app-wallet/div/div[2]/app-deposit-content/div/div[3]')
            address = address_elem.text

            return {
                "address": address,
                "amount": "0.01",
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
