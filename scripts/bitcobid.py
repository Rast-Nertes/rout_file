import requests
from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.imagecaptcha import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://bitcobid.com'
user_email = "alex37347818"
user_password = "JTYYyR2CVJHtxAZ"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

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
    #driver.maximize_window()
    driver.set_window_size(400, 400)

    try:
        driver.implicitly_wait(10)
        driver.execute_script("document.body.style.zoom='400%'")
        driver.execute_script("window.scrollBy(0, 1100);")
        sleep(1.5)
        driver.save_screenshot('captcha.jpg')
        sleep(1.5)
        driver.maximize_window()
        driver.execute_script("document.body.style.zoom='100%'")
    except Exception as e:
        print(f"IMAGE ERROR \n{e}")

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.CSS_SELECTOR, 'tbody > tr > td > table > tbody > tr > td:nth-child(1) > form > table > tbody > tr:nth-child(3) > td:nth-child(2) > input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'tbody > tr > td > table > tbody > tr > td:nth-child(1) > form > table > tbody > tr:nth-child(4) > td:nth-child(2) > input')
        input_password.clear()
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        input_res = driver.find_element(By.CSS_SELECTOR, 'tbody > tr > td > table > tbody > tr > td:nth-child(1) > form > table > tbody > tr:nth-child(5) > td:nth-child(2) > input')
        input_res.clear()
        input_res.send_keys(solve_captcha())
    except Exception as e:
        print(f"ERROR CAPTCHA \n{e}")

    try:
        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td:nth-child(1) > form > table > tbody > tr:nth-child(6) > td:nth-child(2) > input')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"ERROR LOGIN BUTTON \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        sleep(3)
        driver.get('https://bitcobid.com/?a=deposit')

        try:
            driver.implicitly_wait(10)
            ticket = driver.find_element(By.CSS_SELECTOR, 'table > tbody > tr > td > table > tbody > tr > td.bgcolormain > table > tbody > tr > td > div > form > table:nth-child(8) > tbody > tr:nth-child(5) > td > table > tbody > tr > td:nth-child(1) > input[type=radio]')
            sleep(1.5)
            driver.execute_script("arguments[0].click(0);", ticket)

            driver.implicitly_wait(10)
            spend_button = driver.find_element(By.CSS_SELECTOR, 'tbody > tr > td > table > tbody > tr > td.bgcolormain > table > tbody > tr > td > div > form > table:nth-child(8) > tbody > tr:nth-child(6) > td > input')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", spend_button)
        except Exception as e:
            print(f"ERROR TRC20 \n{e}")

        try:
            driver.implicitly_wait(40)
            address = driver.find_element(By.CSS_SELECTOR, '#usdt_form > i > a').text.replace('(Token USDT)', "").replace(" ", '')

            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, '#usdt_form > b').text.replace("USDT", "").replace(" ", "")

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
