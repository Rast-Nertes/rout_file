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


def solve_captcha():
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key("6ab87383c97cb688c42b47e81c96bbcc")

    captcha_text = solver.solve_and_return_solution("captcha.jpg")
    time.sleep(1)

    if captcha_text != 0:
        print("captcha text " + captcha_text)
    else:
        print("task finished with error " + solver.error_code)

    return captcha_text


def login(driver):
    driver.get(url)

    driver.set_window_size(400, 400)
    driver.execute_script("document.body.style.zoom='250%'")
    driver.execute_script("window.scrollBy(0, 660);")
    sleep(1)
    driver.save_screenshot("captcha.jpg")

    solved_captcha = solve_captcha()

    driver.execute_script("document.body.style.zoom='100%'")
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        solved_captcha_input = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td:nth-child(1) > form > table > tbody > tr:nth-child(5) > td:nth-child(2) > input')
        solved_captcha_input.clear()
        solved_captcha_input.send_keys(solved_captcha)
    except Exception as e:
        print(f"SOLVED CAPTCHA ERROR \n{e}")

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td > table > tbody > tr > td:nth-child(1) > form > table > tbody > tr:nth-child(3) > td:nth-child(2) > input')
        input_email.clear()
        input_email.send_keys(user_email)

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
            ticket = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td.bgcolormain > table > tbody > tr > td > div > form > table:nth-child(21) > tbody > tr:nth-child(5) > td > table > tbody > tr > td:nth-child(1) > input[type=radio]')
            sleep(1.4)
            driver.execute_script("arguments[0].click();", ticket)
        except Exception as e:
            print(f"TICKET ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            spend_button = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td.bgcolormain > table > tbody > tr > td > div > form > table:nth-child(21) > tbody > tr:nth-child(6) > td > input')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", spend_button)
        except Exception as e:
            print(f"ERROR SPEND BUTTON \n{e}")

        try:
            driver.implicitly_wait(40)
            address = driver.find_element(By.CSS_SELECTOR, '#usdt_form > i > a').text.replace('(Token USDT)', "").replace(" ", '')

            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td.bgcolormain > table > tbody > tr > td > div > table > tbody > tr:nth-child(8) > td').text

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
