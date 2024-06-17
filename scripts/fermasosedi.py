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

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    api_key = paths[3].strip()
    ext = paths[1].strip()

options.add_extension(ext)


def api_connect(driver):
    sleep(1.5)
    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        sleep(1.5)
        if "2Cap" in driver.title:
            break

    try:
        js_click(driver, 30, '//*[@id="autoSolveRecaptchaV2"]')
        js_click(driver, 30, '//*[@id="autoSolveInvisibleRecaptchaV2"]')
        js_click(driver, 30, '//*[@id="autoSolveRecaptchaV3"]')
        js_click(driver, 30, '//*[@id="autoSolveHCaptcha"]')

        input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        click(driver, 30, '//*[@id="connect"]')
        sleep(4.5)
        driver.switch_to.alert.accept()
    except Exception as e:
        print(f'ERROR CLICK \n{e}')

    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        sleep(1.5)
        if not("2Cap" in driver.title):
            break


def js_click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    driver.execute_script("arguments[0].click();", elem_click)


def wait_visibility(driver, time, XPATH):
    WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.XPATH, XPATH))
    )
    sleep(2.5)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    driver.execute_script("arguments[0].click();", elem_click)


def login(driver):
    api_connect(driver)
    driver.get(url)
    driver.maximize_window()

    try:
        input_data(driver, 45, '//*[@id="username"]', user_name)
        sleep(1)
        input_data(driver, 20, '//*[@id="password"]', user_password)
    except Exception as e:
        print(f'ERROR input data {e} ')

    try:
        time_loop = 0
        while True:
            driver.implicitly_wait(10)
            find_check = driver.find_element(By.XPATH, '//div[@class="captcha-solver-info"]').text
            if ("ена" in find_check) or ("lve" in find_check):
                break
            else:
                if time_loop > 120:
                    return {"status": "0", "ext": "CAPTCHA ERROR"}
                time_loop += 5
                sleep(5)
                print("Wait 5 seconds, captcha solving...")
    except Exception as e:
        print(f'ERROR CHECKBOX \n{e}')

    try:
        click(driver, 30, '//*[@id="login_block"]/div/div[1]/div[2]/div[3]/form/div[4]/input')
    except Exception as e:
        print(f'ERROR LOG BUT \n{e}')


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
            choose_usdt = driver.find_element(By.CSS_SELECTOR, 'div.slist > ul:nth-child(3) > li:nth-child(4)')
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
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)