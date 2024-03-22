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

url = 'http://sexlikereal.com'
user_email = "kiracase34@gmail.com"
user_password = "p4M@yTH@e@5H5QJ"
api_ = '6ab87383c97cb688c42b47e81c96bbcc'

# CHROME CONSTANS

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

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def solve_captcha():

    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(api_)
    solver.set_website_url("https://www.sexlikereal.com/user/login")
    solver.set_website_key("6Lduo_8UAAAAAGvFIr5J2a9BHcgdgyzMyBqrZJck")
    solver.set_soft_id(0)

    g_response = solver.solve_and_return_solution()

    return g_response


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        over_18_button = driver.find_element(By.XPATH, '//*[@id="content"]/div[1]/div/div[4]/button[1]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", over_18_button)
    except Exception as e:
        print(f"ERROR OVER 18 BUTTON \n{e}")
    sleep(2)
    driver.get('https://www.sexlikereal.com/user/login')
    sleep(3)

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.XPATH, '//*[@id="sign--in"]/form/div[1]/div[1]/div[1]/input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '//*[@id="sign--in"]/form/div[1]/div[2]/div[1]/input')
        input_password.clear()
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    try:
        driver.implicitly_wait(20)
        submit_button = driver.find_element(By.XPATH, '//*[@id="sign--in"]/form/div[2]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", submit_button)
    except Exception as e:
        print(f"ERROR SUBMIT BUTTON \n{e}")

    sleep(7.5)
    result_captcha = solve_captcha()

    driver.implicitly_wait(5)
    input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
    driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.XPATH, '//*[@id="sign--in"]/form/div[1]/div[1]/div[1]/input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '//*[@id="sign--in"]/form/div[1]/div[2]/div[1]/input')
        input_password.clear()
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    try:
        driver.implicitly_wait(20)
        submit_button = driver.find_element(By.XPATH, '//*[@id="sign--in"]/form/div[2]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", submit_button)
    except Exception as e:
        print(f"ERROR SUBMIT BUTTON \n{e}")

    while True:
        try:
            driver.implicitly_wait(7)
            error = driver.find_element(By.XPATH, '//*[@id="sign--in"]/form/div[1]/div[4]/div[1]').text

            if error != "":
                sleep(7.5)
                result_captcha = solve_captcha()

                driver.implicitly_wait(5)
                input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
                driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)

                try:
                    driver.implicitly_wait(30)
                    input_email = driver.find_element(By.XPATH, '//*[@id="sign--in"]/form/div[1]/div[1]/div[1]/input')
                    input_email.clear()
                    input_email.send_keys(user_email)

                    driver.implicitly_wait(10)
                    input_password = driver.find_element(By.XPATH, '//*[@id="sign--in"]/form/div[1]/div[2]/div[1]/input')
                    input_password.clear()
                    input_password.send_keys(user_password)

                    driver.implicitly_wait(20)
                    submit_button = driver.find_element(By.XPATH, '//*[@id="sign--in"]/form/div[2]/button')
                    sleep(1.5)
                    driver.execute_script("arguments[0].click();", submit_button)
                except Exception as e:
                    print(f"LOGIN ERROR \n{e}")
        except:
            break

    sleep(3)
    driver.get('https://www.sexlikereal.com/payment/premium')

    try:
        driver.implicitly_wait(10)
        close = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div/div/div[1]/button/span')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", close)
    except Exception as e:
        pass

def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(10)
            choose_payment_method = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/div/div/div/div[2]/div/form/div[1]/div[3]/div[1]/div[2]/div[1]/label')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_payment_method)

            driver.implicitly_wait(10)
            next_step = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/div/div/div/div[2]/div/form/div[1]/div[3]/div[3]/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step)
            sleep(4)
        except Exception as e:
            print(f"ERROR CHOOSE \n{e}")

        try:
            driver.implicitly_wait(20)
            choose_bit_method = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/div/div/div/div[2]/div/form/div[2]/div[1]/div[2]/div[2]/div[7]/label/span/span')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_bit_method)
            try:
                driver.execute_script("arguments[0].click();", choose_bit_method)
            except:
                pass

            driver.implicitly_wait(10)
            submit_button = driver.find_element(By.ID, 'payment_page-btn')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit_button)
        except Exception as e:
            print(f"ERROR SUBMIT \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_usdt = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div/label[8]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_usdt)

            driver.implicitly_wait(10)
            continue_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button)
        except Exception as e:
            print(f"ERROR CHOOSE USDT \n{e}")

        try:
            driver.implicitly_wait(10)
            without_email = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[1]/div[2]/button[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", without_email)

            driver.implicitly_wait(10)
            choose_tron = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[3]/div/div/label[3]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_tron)

            driver.implicitly_wait(10)
            continue_button_2 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div[2]/div/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button_2)
        except Exception as e:
            print(f"ERROR CHOOSE TRON \n{e}")

        driver.set_window_size(1200, 500)

        try:
            driver.implicitly_wait(60)
            amount = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/p').text.replace("USDT", '').replace(" ", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[6]/div/div[2]/div/p').text

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
