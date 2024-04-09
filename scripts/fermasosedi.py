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

url = 'https://fermasosedi.ru/#!/login'
user_email = "rwork875@gmail.com"
user_name = 'rwork875'
user_password = "992l28ja6315"

#992l28ja6315

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
site_key = '6Lf8eygTAAAAAHaMc2B9zckwEiTz4B_VdYthyhGT'

with open('C:/Users/Acer/Desktop/py_scripts/result/ROUT_FILE/config.txt') as file:
    paths = file.readlines()
    api_key = paths[2].strip()

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

    try:
        input_data(driver, 45, '//*[@id="username"]', user_name)
        sleep(1)
        input_data(driver, 20, '//*[@id="password"]', user_password)
    except Exception as e:
        print(f'ERROR ')

    driver.implicitly_wait(30)
    input_captcha_code = driver.find_element(By.ID, 'g-recaptcha-response')
    result_captcha = captcha_solver()
    sleep(1)
    driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)

    try:
        click(driver, 30, '//*[@id="login_block"]/div/div[1]/div[2]/div[3]/form/div[4]/input')
    except Exception as e:
        print(f'ERROR LOG BUT \n{e}')

    while True:
        try:
            driver.implicitly_wait(10)
            sleep(2.5)
            error = driver.find_element(By.XPATH, '/html/body/ul/li/div/div[1]/span').text

            if "Проверка" in error:
                result_captcha = captcha_solver()
                driver.implicitly_wait(5)
                input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
                sleep(1)
                driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)
                sleep(1.5)
                click(driver, 30, '//*[@id="login_block"]/div/div[1]/div[2]/div[3]/form/div[4]/input')
            else:
                break
        except:
            break


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            click(driver, 30, '//*[@id="menu_d03"]')
            sleep(1)
            click(driver, 20, '//*[@id="bi_l2_balance"]/ul/li[1]/a')
        except Exception as e:
            print(f'ERROR APPEND \n{e}')

        try:
            click(driver, 20, '//*[@id="js-body"]/div[2]/div[4]/div/div[2]/div/div/a[1]/img')
        except Exception as e:
            print(f'ERROR CLICK PAY \n{e}')

        try:
            input_data(driver, 30, '//*[@id="js-body"]/div[2]/div[4]/div/div[2]/div/div/label/input', '650')
            sleep(1)
            click(driver, 20, '//*[@id="js-body"]/div[2]/div[4]/div/div[2]/div/div/button')
        except Exception as e:
            print(f'ERROR INPUT AMOUNT \n{e}')

        try:
            click(driver, 20, '/html/body/div[3]/div[2]/div[3]/button[2]')
        except Exception as e:
            print(f'ERROR NEXT BUT \n{e}')

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
