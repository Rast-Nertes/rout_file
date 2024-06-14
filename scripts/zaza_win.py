from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://zaza.win/auth/login'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
options.add_argument("--disable-save-password-bubble")
options.add_argument('--log-level=3')
options.add_argument('--disable-remote-fonts')
options.add_experimental_option('prefs', {'intl.accept_languages': 'en, en_US'})

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
        input_data(driver, 60, '//input[@type="login"]', user_email)
        input_data(driver, 30, '//input[@type="password"]', user_password)
        click(driver, 30, '(//button[@type="button"])[3]')
    except Exception as e:
        return {"status": "0", "ext": f"error login {e}"}

    sleep(4.5)
    driver.get('https://zaza.win/cashier/deposit')

    try:
        click(driver, 30, '//img[@class="item__icon Tether TRC-20"]')
    except Exception as e:
        return {"status":"0", "ext":f"error choose trc20: {e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//p[@class="crypto-flow__bottom-text crypto-flow__bottom-text--account"]')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//p[@class="crypto-flow__bottom-text"]')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("Min.", '').replace("deposit", '').replace(":", '').replace("USDTT", '').replace("\xa0", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
