from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://moneygnomes.store/login'
user_email = "kiracase34@gmail.com"
user_password = "kirakira555"
site_key = '6LekzaEpAAAAALMtzRGBt95GP4QpM83jEstyePbA'

# CHROME CONSTANS

# with open('config.txt') as file:
#     paths = file.readlines()
#     api_key = paths[2].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


# def captcha_solver():
#     solver = recaptchaV2Proxyless()
#     solver.set_verbose(1)
#     solver.set_key(api_key)
#     solver.set_website_url(url)
#     solver.set_website_key(site_key)
#     solver.set_soft_id(0)
#
#     g_response = solver.solve_and_return_solution()
#     return g_response


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
    #
    # sleep(3.5)
    # result_captcha = captcha_solver()
    # driver.implicitly_wait(4.5)
    # input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
    # driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)

    try:
        driver.implicitly_wait(50)
        input_email = driver.find_element(By.XPATH, '/html/body/div[1]/center/div[2]/div[1]/form/table[2]/tbody/tr[1]/td[2]/input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(30)
        input_password = driver.find_element(By.XPATH, '/html/body/div[1]/center/div[2]/div[1]/form/table[2]/tbody/tr[2]/td/input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '/html/body/div[1]/center/div[2]/div[1]/form/table[2]/tbody/tr[3]/td/input')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    sleep(3.5)
    driver.get('https://moneygnomes.store/account/insert')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(20)
            choose_free = driver.find_element(By.XPATH, "/html/body/div/center/div[2]/div[2]/b/table/tbody/tr/td[2]")
            sleep(2)
            choose_free.click()
        except Exception as e:
            print(f"ERROR CHOOSE FREEKASSA \n{e}")

        try:
            input_data(driver, 20 , '//*[@id="oa"]', '650')
            sleep(1)
            click(driver, 20, '//*[@id="submit"]')
            sleep(1)
            click(driver, 20, '/html/body/div/center/div[2]/div[2]/b/center/form/input[8]')
        except Exception as e:
            print(f"ERROR INPUT AMOUNT \n{e}")

        try:
            driver.implicitly_wait(60)
            choose_trc20 = driver.find_element(By.ID, 'currency-15')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(40)
            input_email = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[1]/div/form/div/div[2]/input')
            input_email.clear()
            input_email.send_keys(user_email)
        except Exception as e:
            print(f"INPUT EMAIL \n{e}")

        try:
            driver.implicitly_wait(60)
            submit_payment = driver.find_element(By.ID, 'submit-payment')
            sleep(1.5)
            submit_payment.click()
        except Exception as e:
            print(f"SUBMIT ERROR \n{e}")

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[7]/div[2]').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[5]/span').text

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