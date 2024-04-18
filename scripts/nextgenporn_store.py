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

url = 'https://nextgenporn-store.net/product/futasys-sexercise-bundle/'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    api_key = paths[2].strip()

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


def captcha_solver():
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(api_key)
    solver.set_website_url(url)
    solver.set_website_key(site_key)
    solver.set_soft_id(0)

    g_response = solver.solve_and_return_solution()
    return g_response


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
        click(driver, 20, '//*[@id="wptp-form"]/div/input[1]')
    except:
        pass

    try:
        click(driver, 20, '//*[@id="product-4450"]/div[2]/form/button')
        sleep(2)
        click(driver, 30, '//*[@id="woofc-area"]/div[3]/div[4]/div/div[2]/a')
    except Exception as e:
        print(f'ERROR BUY NOW \n{e}')

    try:
        input_data(driver, 40, '//*[@id="billing_first_name"]', "Kira")
        input_data(driver, 30, '//*[@id="billing_last_name"]', "Ivanova")
        input_data(driver, 30, '//*[@id="billing_email"]', user_email)
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    try:
        driver.implicitly_wait(30)
        driver.execute_script("window.scrollBy(0, 500);")
        sleep(3.5)
        click_submit = driver.find_element(By.ID, 'place_order')
        sleep(1)
        click_submit.click()
    except Exception as e:
        print(f'ERROR PLACE ORDER \n{e}')

    try:
        click(driver, 80, '//label[@data-test="Tether-currency"]')
        sleep(1)
        click(driver, 50, '//button[@data-test="continue-button"]')
    except Exception as e:
        print(f'ERROR CHOOSE TETHER \n{e}')

    try:
        input_data(driver, 30, '//input[@data-test="input-email"]', user_email)
        sleep(1)
        click(driver, 50, '//button[@data-test="continue-button"]')
    except Exception as e:
        print(f'ERROR INPUT EMAIL \n{e}')

    try:
        click(driver, 50, '//label[@data-test="Tron-currency"]')
        sleep(1)
        click(driver, 50, '//button[@data-test="continue-button"]')
    except Exception as e:
        print(f'ERROR CHOOSE TETHER \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        sleep(2)
        driver.set_window_size(1000, 700)
        try:
            sleep(1.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[6]/div/div[2]/div/p').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/p').text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)