from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://hugewin.com/en'
user_email = "kiracase34"
user_password = "QLE94#2c.ti$AQw"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_argument("--auto-open-devtools-for-tabs")

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
        click(driver, 80, '//*[@id="wrapper"]/header/div[1]/div[2]/div[2]/a[1]')
        input_data(driver, 40, '//*[@id="account-menu"]/div/form/div[1]/input', user_email)
        input_data(driver, 20, '//*[@id="account-menu"]/div/form/div[2]/input', user_password)
        click(driver, 20, '//*[@id="account-menu"]/div/form/input')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    sleep(2.5)
    driver.get('https://hugewin.com/en/deposit')

    try:
        driver.implicitly_wait(50)
        get_href = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div/section[2]/section/div[1]/div/div/div[2]/div/div[2]/div/table/tbody/tr[1]/td[3]/div/a').get_attribute('href')
        driver.get(get_href)
    except Exception as e:
        find_input_tag = driver.find_element(By.XPATH, '//*[@id="account-menu"]/div/form/div[1]/input')
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"ERROR DEPOS BUT \n{e}")

    try:
        click(driver, 80 , '//*[@id="cdk-step-content-1-0"]/div[6]/button[3]')
        click(driver, 20, '//*[@id="cdk-step-content-1-0"]/div[7]/button')
    except Exception as e:
        print(f"ERROR CHOOSE TRC20 \n{e}")

    try:
        input_data(driver, 20, '//*[@id="mat-input-1"]', '1')
        click(driver, 20, '//*[@id="cdk-step-content-1-0"]/div[7]/button')
    except Exception as e:
        print(f'ERROR INPUT AMOUNT \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '//*[@id="cdk-step-content-1-1"]/div[2]/div/div[1]/p[2]').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '//*[@id="cdk-step-content-1-1"]/div[3]/div/div[1]/p[2]').text

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
