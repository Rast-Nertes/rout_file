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

url = 'https://wazbee.casino/auth/sign-in'
user_email = "kiracase34@gmail.com"
user_password = "ArN6W!5ju7HWT3N"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
# options.add_argument('--headless')

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
        input_data(driver, 30, '/html/body/app-root/app-auth/div/div/div/app-simple-sign-in/div/div[2]/form/app-text-field/div/input', user_email)
        input_data(driver, 30, '/html/body/app-root/app-auth/div/div/div/app-simple-sign-in/div/div[2]/form/app-text-field-password/div[1]/div/input', user_password)
        click(driver, 30, '/html/body/app-root/app-auth/div/div/div/app-simple-sign-in/div/div[2]/form/div/button')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        click(driver, 20, '(/html/body/app-root/app-pages/app-side-nav/nav/div[2]/div[1]/app-user-balance/div[1]/div)[2]')
    except:
        driver.implicitly_wait(10)
        find_input_tag = driver.find_element(By.XPATH, '/html/body/app-root/app-auth/div/div/div/app-simple-sign-in/div/div[2]/form/app-text-field-password/div[1]/div/input')
        if find_input_tag:
            return "Login error."

    try:
        sleep(1.5)
        click(driver, 20, '//img[@alt="USDT TRC20"]')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    try:
        sleep(1.5)
        input_data(driver, 20, '//*[@id="depositSumInput"]', '10')
        click(driver, 20, '//*[@id="depositBtn"]/button')
    except Exception as e:
        print(f'ERROR INPUT AMOUNT \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        log = login(driver)
        if log:
            return "Login error. Check script."

        driver.implicitly_wait(10)
        find_frame = driver.find_element(By.ID, 'paymentForm')
        sleep(0.6)
        driver.switch_to.frame(find_frame)

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '//*[@id="cryptoAddress"]').get_attribute("value")

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '//*[@id="amount"]').get_attribute('value')

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
