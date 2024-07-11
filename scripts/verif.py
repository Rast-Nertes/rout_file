from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://verif.work/signin'
user_email = "kiracase34@gmail.com"
user_password = "fuz84w!jFmfRiVD"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def solve_captcha():
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key("6ab87383c97cb688c42b47e81c96bbcc")
    solver.set_website_url(url)
    solver.set_website_key("6Lcf7bcZAAAAANLiSU7DSfOcXFbAVzs9fXLaoZht")
    solver.set_soft_id(0)

    g_response = solver.solve_and_return_solution()
    return g_response


def login(driver):
    driver.get(url)
    driver.maximize_window()

    driver.implicitly_wait(5)
    input_loginform = driver.find_element(By.ID, 'loginform-recaptcha')
    driver.execute_script("arguments[0].removeAttribute('type')", input_loginform)

    captcha_code = solve_captcha()

    input_loginform.send_keys(captcha_code)

    driver.implicitly_wait(5)
    input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
    driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, captcha_code)
    sleep(1.5)

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.ID, 'loginform-email')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.ID, 'loginform-password')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, '#login-form > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
        sleep(10)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    sleep(3)
    driver.get('https://verif.work/cabinet/balance/refill')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        while True:
            try:
                driver.implicitly_wait(10)
                error_text = driver.find_element(By.CSS_SELECTOR, '#login-form > div.form-group.field-loginform-recaptcha.has-error > p').text
                if "Подтвердите" in error_text:
                    login(driver)
            except:
                break

        try:
            driver.implicitly_wait(60)
            input_amount = driver.find_element(By.XPATH, '//*[@id="form"]/div[1]/input')
            input_amount.clear()
            input_amount.send_keys('1000')

            driver.implicitly_wait(30)
            choose_usdt_trc20 = driver.find_element(By.CSS_SELECTOR, '#form > div:nth-child(3) > div > div:nth-child(4) > label')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_usdt_trc20)

            driver.implicitly_wait(30)
            place_order = driver.find_element(By.CSS_SELECTOR, 'div.content-area > div > div.row > div.col-lg-7.col-xs-12 > div > div > div.col-xs-12.text-center > button')
            driver.execute_script("arguments[0].click();", place_order)
        except Exception as e:
            print(f"ERROR CHOOSE TRC20 \n{e}")

        try:
            driver.implicitly_wait(30)
            address = driver.find_element(By.ID, 'wallet').get_attribute('value')

            driver.implicitly_wait(10)
            amount = driver.find_element(By.ID, 'sum').get_attribute('value')

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
