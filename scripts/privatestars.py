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

url = 'https://www.private.com/site/private-stars/'
user_email = "yewoxo4550@otemdi.com"
user_password = "Qwerty62982"
site_key = '6LcMtcEmAAAAAJjCjEXV23xbWKozOMZBmC7Ft3rw'

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    api_key = paths[2].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}

#Funct


def captcha_solver(URL):
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(api_key)
    solver.set_website_url(URL)
    solver.set_website_key(site_key)
    solver.set_soft_id(0)

    g_response = solver.solve_and_return_solution()
    return g_response


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1)
    driver.execute_script("arguments[0].click();", elem_click)
    sleep(1)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


#Script


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        accept_cookie = driver.find_element(By.ID, 'accept_all_cookies')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", accept_cookie)
    except:
        pass

    try:
        driver.implicitly_wait(35)
        login_butt = driver.find_element(By.ID, 'MEMBERS')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_butt)
    except Exception as e:
        print(f'ERROR LOG BUTTON \n{e}')

    sleep(3.5)
    result_captcha = captcha_solver(driver.current_url)
    driver.implicitly_wait(6.5)
    input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
    driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)

    try:
        input_data(driver, 30, '//*[@id="inputUsername3"]', user_email)
        sleep(1.5)
        input_data(driver, 30, '//*[@id="inputPassword3"]', user_password)
    except Exception as e:
        print(f"ERROR INPUT DATA \n{e}")

    try:
        click(driver, 20, '//*[@id="main_form"]/div/div[4]/div/button[1]')
    except Exception as e:
        print(f"ERROR LOG BUT \n{e}")

    input("Press")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR, '').text

            driver.implicitly_wait(10)
            amount = driver.find_element(By.CSS_SELECTOR, '').text

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