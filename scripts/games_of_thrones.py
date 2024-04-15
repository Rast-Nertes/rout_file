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

url = 'https://games-of-thrones.com/login'
user_email = "kiracase34@gmail.com"
user_password = "RBbH$tG$am49AZY"
site_key = '6LfB0fAoAAAAAGh_HziuH-kUo3Qay30h-9IiNrde'

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

    sleep(3.5)
    result_captcha = captcha_solver()
    driver.implicitly_wait(5.5)
    input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
    driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)

    try:
        input_data(driver, 20, '//input[@type="text"]', user_email)
        input_data(driver, 20, '//input[@type="password"]', user_password)

        driver.implicitly_wait(10)
        log_but = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[6]/center/div/div/button/div[2]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", log_but)
    except Exception as e:
        print(f'ERROR LOG \n{e}')

    while True:
        try:
            sleep(1.5)
            driver.implicitly_wait(10)
            find_error = driver.find_element(By.XPATH, '//*[@id="btu-prompt-login_required"]/div/div[2]/p').text
            if "failed" in find_error:
                driver.implicitly_wait(5)
                driver.find_element(By.XPATH, '//*[@id="btu-prompt-login_required"]/div/div[2]/div/div[1]/div/button').click()

                result_captcha = captcha_solver()
                driver.implicitly_wait(5.5)
                input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
                driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)

                input_data(driver, 20, '//input[@type="text"]', user_email)
                input_data(driver, 20, '//input[@type="password"]', user_password)

                driver.implicitly_wait(10)
                log_but = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[6]/center/div/div/button/div[2]')
                sleep(1.5)
                driver.execute_script("arguments[0].click();", log_but)
            else:
                print(f"Solve")
                break
        except:
            break

    try:
        click(driver, 20, '//*[@id="btu-prompt-login_required"]/div/div[2]/div/div[1]/div/button/div[1]')
    except:
        pass

    try:
        click(driver,20, '/html/body/div[7]/div[4]/div[1]/div/div[17]')
    except Exception as e:
        print(f"ERROR ADD BALANCE \n{e}")

    try:
        click(driver, 20, '//button[@class="psusdt"]')
    except Exception as e:
        print(f'ERROR CHOOSE CRYPTO PAYMENT \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '//*[@id="main_deposit_address"]').get_attribute('value')

            return {
                "address": address,
                "amount": "0.01",
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
