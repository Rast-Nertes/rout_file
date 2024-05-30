from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://primexbt.com/id/sign-in?_lang=en'
user_email = "kejokan542@haislot.com"
user_password = "Qwerty17"

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

options.add_extension(ext)
# options.binary_location = chrome_path

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000
#
# proxy_address = "196.19.121.187"
# proxy_login = 'WyS1nY'
# proxy_password = '8suHN9'
# proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def api_connect(driver):
    sleep(1.5)
    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        print(driver.title)
        sleep(1.5)
        if "2Cap" in driver.title:
            break

    try:
        click(driver, 30, '//*[@id="autoSolveRecaptchaV2"]')
        click(driver, 30, '//*[@id="autoSolveInvisibleRecaptchaV2"]')
        input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        click(driver, 30, '//*[@id="connect"]')
        sleep(4.5)
        driver.switch_to.alert.accept()
    except Exception as e:
        print(f'ERROR CLICK \n{e}')

    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        print(driver.title)
        sleep(1.5)
        if not("2Cap" in driver.title):
            break


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
    api_connect(driver)

    driver.get(url)
    driver.maximize_window()
    actions = ActionChains(driver)

    try:
        input_data(driver, 30, '//*[@id="mat-input-0"]', user_email)
        input_data(driver, 30, '//*[@id="mat-input-1"]', user_password)
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    sleep(1.5)

    try:
        click(driver, 30, '/html/body/prm-root/id-id/div/div/ng-component/form/div[3]/button/span[3]')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    sleep(4.5)
    driver.get('https://primexbt.com/my/accounts/deposit/crypto')

    try:
        click(driver, 30, '//*[@id="mat-select-value-1"]')
        click(driver, 30, '//*[@id="mat-option-7"]/span')
    except Exception as e:
        print(f'ERROR CHOOSE USDT \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '/html/body/prm-root/prm-my/prm-no-sidebar-layout/div/div/prm-home/prm-deposit-crypto/div/prm-deposit-crypto-flow/div/div[2]/form/xbt-stepper/div[4]/div[2]/div/div/div/prm-deposit-account/div/div[2]/div[1]/span[2]')
            address = address_elem.text

            # driver.implicitly_wait(30)
            # amount_elem = driver.find_element(By.XPATH, '//*[@id="step_pay__amount_payTo"]')
            # amount = amount_elem.text

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