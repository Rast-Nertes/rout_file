from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.imagecaptcha import *
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://luxioprofit.com/'
user_email = "alex37347818"
user_password = "JTYYyR2CVJHtxAZ"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

#PROXY_CONSTANS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@45.130.254.133:8000",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[2].strip()
    ext = paths[1].strip()


def solve_captcha():
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(api_key)

    captcha_text = solver.solve_and_return_solution("captcha.jpg")
    time.sleep(1)

    if captcha_text != 0:
        print("captcha text " + captcha_text)
    else:
        print("task finished with error " + solver.error_code)

    return captcha_text


def login(driver):
    driver.get(url)
    driver.maximize_window()

    while True:

        try:
            driver.implicitly_wait(5)
            driver.find_element(By.XPATH, '/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr/td[1]/form/table/tbody/tr[5]/td[1]/img').screenshot('captcha.jpg')
            solved_captcha = solve_captcha()
        except:
            break

        try:
            driver.implicitly_wait(10)
            solved_captcha_input = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td:nth-child(1) > form > table > tbody > tr:nth-child(5) > td:nth-child(2) > input')
            solved_captcha_input.clear()
            solved_captcha_input.send_keys(solved_captcha)
        except Exception as e:
            print(f"SOLVED CAPTCHA ERROR \n{e}")

        try:
            sleep(2.5)
            driver.implicitly_wait(30)
            input_email = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td > table > tbody > tr > td:nth-child(1) > form > table > tbody > tr:nth-child(3) > td:nth-child(2) > input')
            input_email.clear()
            input_email.send_keys(user_email)

            sleep(1.5)
            driver.implicitly_wait(10)
            input_password = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td > table > tbody > tr > td:nth-child(1) > form > table > tbody > tr:nth-child(4) > td:nth-child(2) > input')
            input_password.clear()
            input_password.send_keys(user_password)

            driver.implicitly_wait(10)
            login_button = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td > table > tbody > tr > td:nth-child(1) > form > table > tbody > tr:nth-child(6) > td:nth-child(2) > input')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", login_button)
        except Exception as e:
            print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)
        sleep(3)

        driver.get('https://luxioprofit.com/?a=deposit')
        try:
            driver.implicitly_wait(10)
            accept_choose_trc20 = driver.find_element(By.XPATH, '//input[@name="type"]')
            sleep(1.5)
            accept_choose_trc20.click()

            driver.implicitly_wait(10)
            ticket = driver.find_element(By.XPATH, '(//input[@name="h_id"])[2]')
            sleep(1.4)
            driver.execute_script("arguments[0].click();", ticket)
        except Exception as e:
            print(f"TICKET ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            spend_button = driver.find_element(By.XPATH, '//input[@class="sbmt"]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", spend_button)
        except Exception as e:
            print(f"ERROR SPEND BUTTON \n{e}")

        try:
            driver.implicitly_wait(20)
            data_elem = driver.find_element(By.XPATH, '//*[@id="deposit_result_div"]').get_attribute('src')

            address = data_elem.split("wallet/")[1].split('/amount')[0]
            amount = data_elem.split('amount/')[1].split('/')[0]

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)