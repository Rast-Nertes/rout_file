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

url = 'https://superbirds.ink'
user_email = "kiracase34@gmail.com"
user_password = "zV68G8dKSnkYXXy"
site_key = '6Lc3r6UpAAAAAIzszcms9DbKoLhiSl0PqaV63dw9'

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    api_key = paths[2].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def captcha_solver():
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(api_key)
    solver.set_website_url(url)
    solver.set_website_key(site_key)
    solver.set_soft_id(0)

    g_response = solver.solve_and_return_solution()
    return g_response


def login(driver):
    driver.get(url)
    driver.maximize_window()

    sleep(3.5)
    result_captcha = captcha_solver()
    driver.implicitly_wait(7.5)
    input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
    driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)

    try:
        driver.implicitly_wait(50)
        input_email = driver.find_element(By.XPATH, '//*[@id="loginste"]/input[1]')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(30)
        input_password = driver.find_element(By.XPATH, '//*[@id="loginste"]/input[2]')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '//*[@id="loginste"]/input[3]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    while True:
        try:
            driver.implicitly_wait(6.5)
            find_error = driver.find_element(By.XPATH, '//*[@id="loginste"]/p/b').text
            sleep(1.5)
            if "Ошибка" in find_error:

                result_captcha = captcha_solver()

                driver.implicitly_wait(7.5)
                input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
                driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)
                sleep(2.5)

                driver.implicitly_wait(50)
                input_email = driver.find_element(By.XPATH, '//*[@id="loginste"]/input[1]')
                input_email.clear()
                input_email.send_keys(user_email)

                driver.implicitly_wait(30)
                input_password = driver.find_element(By.XPATH, '//*[@id="loginste"]/input[2]')
                input_password.clear()
                input_password.send_keys(user_password)

                driver.implicitly_wait(10)
                login_button = driver.find_element(By.XPATH, '//*[@id="loginste"]/input[3]')
                sleep(1.5)
                driver.execute_script("arguments[0].click();", login_button)
            else:
                break
        except:
            break

    sleep(3.5)
    driver.get('https://superbirds.ink/account/insert')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(40)
            input_amoun = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/form/center/input[1]')
            input_amoun.clear()
            input_amoun.send_keys("650")

            driver.implicitly_wait(30)
            choose_free = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/form/center/div[1]/div[3]/input')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_free)

            driver.implicitly_wait(30)
            next_step_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/form/center/input[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step_button)
        except Exception as e:
            print(f"ERROR CHOOSE FREEKASSA \n{e}")

        try:
            driver.implicitly_wait(30)
            step_2 = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div[2]/div/div[2]/center/a/input')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", step_2)
        except Exception as e:
            print(f"SWITCH ERROR \n{e}")

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
