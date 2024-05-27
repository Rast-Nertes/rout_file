from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://www.bet2u2.com/en/'
user_email = "kiracase34@gmail.com"
user_password = "Kiramira123"

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
    # api_connect(driver)
    driver.get(url)

    try:
        click(driver, 30, '//button[@class="btn s-small sign-in "]')
    except Exception as e:
        return {"status": "0", "ext": f"error log in button {e}"}

    try:
        input_data(driver, 30, '//input[@name="username"]', user_email)
        input_data(driver, 30, '//input[@name="password"]', user_password)
        click(driver, 30, '//button[@class="btn a-color "]')
    except Exception as e:
        return {"status":"0", "ext":f"error login {e}"}

    sleep(6.5)
    driver.get('https://www.bet2u2.com/en/?profile=open&account=balance&page=deposit&selectedGroup=all&selectedMethod=%20B2pay11')

    try:
        sleep(2.5)
        input_data(driver, 30, '//input[@name="amount"]', '5')
        click(driver, 30, '//button[@class="btn a-color deposit "]')
    except Exception as e:
        return {"status":"0", "ext":f"error input min amount {e}"}

    try:
        sleep(1.5)
        click(driver, 30, '(//button[@class="a-tile-button tile-button"])[4]')
        click(driver, 30, '//button[@class="a-button button defined-payway__button primary"]')
    except Exception as e:
        return {"status":"0", "ext":f"error click trc20 {e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//span[@class="clipboard-button__element"]')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//span[@class="payment__amount"]')
            amount = amount_elem.text

            return {
                "address": address.replace(" ", ''),
                "amount": amount.replace("USDT", '').replace("(5 USD)", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
