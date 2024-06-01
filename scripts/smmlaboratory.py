from time import sleep
from flask import jsonify
from seleniumwire import webdriver
from anticaptchaofficial.imagecaptcha import *
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://smmlaboratory.com'
user_login = 'kiracase34@gmail.com'
user_password = 'kirakira123'

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[2].strip()
    ext = paths[1].strip()

#CHROME OPTIONS

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False
chrome_options.add_argument('--disable-blink-features=AutomationControlled')


def js_click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    driver.execute_script("arguments[0].click();", elem_click)


def solve_captcha():
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(api_key)

    solver.set_soft_id(0)

    captcha_text = solver.solve_and_return_solution("captcha.jpeg")
    return captcha_text


def login(driver):
    driver.get(url)
    driver.maximize_window()

    sleep(3.5)
    while True:
        try:
            driver.implicitly_wait(5)
            driver.find_element(By.XPATH, '//*[@id="captcha_image"]').screenshot("captcha.jpeg")

            result_captcha = solve_captcha()

            driver.implicitly_wait(10)
            input_captcha = driver.find_element(By.XPATH, '//*[@id="captcha_input"]')
            input_captcha.send_keys(result_captcha)

            driver.implicitly_wait(10)
            submit = driver.find_element(By.XPATH, '//*[@id="submit_button"]')
            submit.click()
        except Exception as e:
            print('solve')
            break

    try:
        #Клик для входа
        element_click = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="accaunt"]'))
        )
        element_click.click()

        #Вводим логин

        element_start__input_user_login = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.ID, 'email'))
        )
        element_start__input_user_login.send_keys(user_login)

        #Вводим пароль

        input_user_password = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'password'))
        )
        input_user_password.send_keys(user_password)

        #Заходим

        accept_registration = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="register-box"]/div[1]/button[1]'))
        )
        accept_registration.click()

        sleep(5)

    except Exception as e:
        print(f"LOGIN ERROR -- \n{e}")


def get_wallet_data():
    with webdriver.Chrome(options=chrome_options) as driver:
        login(driver)

        driver.get('https://smmlaboratory.com/money/wallet/')
        try:
            add_to_cart = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[9]/div[2]/div[2]/div[4]/button'))
            )
            add_to_cart.click()

            basket = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/nav/a[2]/div[1]'))
            )
            basket.click()
        except Exception as e:
            print(f'ERROR ADD TO BUSKET \n{e}')

        try:
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="for-button-submit"]/div[3]/div/label[2]/div'))
            )
            js_click(driver, 10, '//*[@id="for-button-submit"]/div[3]/div/label[2]/div')

            sleep(5)

            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[9]/div/div/div[4]/div[1]/input'))
            )
            js_click(driver, 10, '/html/body/div[2]/div[9]/div/div/div[4]/div[1]/input')
        except Exception as e:
            print(f'ERROR CHOOSE METHOD \n{e}')

        try:
            choose_wallet = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]'))
            )
            choose_wallet.click()

            choose_trc20 = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[2]/ul/li[1]'))
            )
            choose_trc20.click()

            sleep(1.5)
            js_click(driver, 10, '//*[@id="root"]/div/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div[1]')
            js_click(driver, 10, '/html/body/div[1]/div/div[1]/div/div[1]/div/div[3]/div/div/div[2]/div[2]/ul/li[2]')
        except Exception as e:
            print(f'ERROR CHOOSE TRC20 \n{e}')

        try:
            next_step = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div/div[1]/div/div[3]/div/button'))
            )
            next_step.click()
        except Exception as e:
            print(f'ERROR NEXT STEP BUTTON \n{e}')

        try:
            amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="root"]/div/div[1]/div/div[1]/div/div[2]/div[2]/div[1]/div[1]/div/span[1]'))
            )
            amount = amount.text.replace("USDT", "")

            address = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//span[@class="address__text"]'))
            )
            address = address.text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f'ERROR DATA \n{e}')


def wallet():
    wallet_data = get_wallet_data()
    print(wallet_data)
    return jsonify(wallet_data)
