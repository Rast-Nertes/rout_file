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
#33775511l
url = 'https://robots-game.org/ru/login'
user_email = "kiracase34@gmail.com"
user_password = "vY7psYYKvCZTsG3"
site_key = '6Lfq3TEUAAAAABhXFKk_qsch6OfG7AcKspdUartK'

# CHROME CONSTANS

proxy_address = "62.3.13.13"
proxy_login = '1QjtPL'
proxy_password = 'pHSyxy'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}

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

    result_captcha = captcha_solver()
    driver.implicitly_wait(7.5)
    input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
    driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)

    try:
        driver.implicitly_wait(50)
        input_email = driver.find_element(By.XPATH, '//*[@id="login"]/div[2]/form/label[1]/input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '//*[@id="login"]/div[2]/form/label[2]/input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '//*[@id="login"]/div[2]/form/div[2]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    while True:
        try:
            driver.implicitly_wait(7.5)
            find_error = driver.find_element(By.XPATH, 'body > div.message.message--type_warning.message--visible_show').text
            sleep(1)

            if "робот" in find_error:

                result_captcha = captcha_solver()

                driver.implicitly_wait(7.5)
                input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
                driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)
                sleep(2.5)

                driver.implicitly_wait(50)
                input_email = driver.find_element(By.XPATH, '//*[@id="login"]/div[2]/form/label[1]/input')
                input_email.clear()
                input_email.send_keys(user_email)

                driver.implicitly_wait(10)
                input_password = driver.find_element(By.XPATH, '//*[@id="login"]/div[2]/form/label[2]/input')
                input_password.clear()
                input_password.send_keys(user_password)

                driver.implicitly_wait(10)
                login_button = driver.find_element(By.XPATH, '//*[@id="login"]/div[2]/form/div[2]/button')
                sleep(1.5)
                driver.execute_script("arguments[0].click();", login_button)
            else:
                break
        except:
            break
    sleep(3)
    driver.get('https://robots-game.org/ru/account/insert')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(40)
            input_amoun = driver.find_element(By.XPATH, '//*[@id="payblock"]/label/input')
            input_amoun.clear()
            input_amoun.send_keys("550")

            driver.implicitly_wait(30)
            choose_pay = driver.find_element(By.XPATH, '//*[@id="accountinsert"]/div[2]/div[3]/div[2]/div/form[2]/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_pay)
        except Exception as e:
            print(f"ERROR CHOOSE FREEKASSA \n{e}")

        try:
            sleep(5.5)
            driver.switch_to.window(driver.window_handles[1])
            driver.refresh()
            sleep(2)
        except Exception as e:
            print(f"SWITCH ERROR \n{e}")

        try:
            driver.implicitly_wait(50)
            choose_usdt = driver.find_element(By.CSS_SELECTOR, 'div.slist > ul:nth-child(3) > li:nth-child(3)')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_usdt)

            driver.implicitly_wait(50)
            input_email = driver.find_element(By.ID, 'id_order_email')
            input_email.clear()
            input_email.send_keys(user_email)

            driver.implicitly_wait(40)
            place_order = driver.find_element(By.XPATH, '/html/body/div/form/div[2]/div[4]/div[2]/a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", place_order)
        except Exception as e:
            print(f'ERROR CHOOSE USDT \n{e}')

        try:
            sleep(2.5)
            driver.implicitly_wait(90)
            address = driver.find_element(By.CSS_SELECTOR, 'div.amount__info.bb-info.attantion.blue-atantion > h3 > font:nth-child(6)').text

            driver.implicitly_wait(60)
            amount = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[1]/h3/font[1]').text.replace("USDT", '').replace(" ", '')

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
