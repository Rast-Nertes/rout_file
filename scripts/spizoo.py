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

url = 'https://www.spizoo.com/'
user_email = "yewoxo4550@otemdi.com"
user_email_2 = "yewoxo12@gmail.com"
user_password = "Qwerty62982"
site_key = '6LfbstoZAAAAAJtuOrbPAaMDaW7gNy45Qx_xCuOk'

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    api_key = paths[2].strip()

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def captcha_solver(URL):
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(api_key)
    solver.set_website_url(URL)
    solver.set_website_key(site_key)
    solver.set_soft_id(0)

    g_response = solver.solve_and_return_solution()
    return g_response


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1)
    driver.execute_script("arguments[0].click();", elem_click)
    sleep(1)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


def login(driver):
    actions = ActionChains(driver)
    driver.get(url)
    driver.maximize_window()

    try:
        click(driver, 10, '//*[@id="agreement-pup"]/div/div[3]/div/button[2]')
        sleep(2.5)
    except Exception as e:
        print(f"ERROR ACCEPT COOKIE \n{e}")

    try:
        click(driver, 35, '//*[@id="security-auth-msg"]/div/a[2]/div')
    except Exception as e:
        print(f"ERROR JOIN \n{e}")

    try:
        click(driver, 30, '//*[@id="content"]/form/div/div[1]/label[3]')

        input_email = driver.find_element(By.ID, 'InputEmail')
        input_email.clear()
        input_email.send_keys(user_email)
    except Exception as e:
        print(f"ERROR CHOOSE CRYPTO \n{e}")

    result_captcha = captcha_solver(driver.current_url)
    driver.implicitly_wait(7.5)
    input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
    driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)

    try:
        click(driver, 30, '//*[@id="content"]/form/div/button')
    except Exception as e:
        print(f"ERROR CONTINUE \n{e}")

    while True:
        try:
            sleep(3.5)
            driver.implicitly_wait(10.5)
            find_error = driver.find_element(By.XPATH, '//*[@id="content"]/form/div/fieldset/div/div[1]').text

            if "failed" in find_error:

                result_captcha = captcha_solver(driver.current_url)

                driver.implicitly_wait(7.5)
                input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
                driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result_captcha)
                sleep(2.5)

                click(driver, 30, '//*[@id="content"]/form/div/div[1]/label[3]')
                sleep(1.5)
                input_email = driver.find_element(By.ID, 'InputEmail')
                input_email.clear()
                input_email.send_keys(user_email)
                sleep(1.5)
                click(driver, 30, '//*[@id="content"]/form/div/button')
            else:
                print("CAPTCHA solved")
                break
        except:
            break

    try:
        driver.implicitly_wait(50)
        next_step = driver.find_element(By.ID, 'CryptoPurchaseButton')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", next_step)
    except Exception as e:
        print(f'ERROR NEXT \n{e}')

    try:
        driver.implicitly_wait(30)
        select_crypto = driver.find_element(By.ID, 'CryptoPopupSelectWalletDdl')
        sleep(1.5)
        select_crypto.click()

        actions.send_keys(Keys.ARROW_DOWN).perform()
    except Exception as e:
        print(f'ERROR SELECT \n{e}')

    try:
        driver.implicitly_wait(10)
        select_trc20 = driver.find_element(By.ID, 'CryptoPopupSelectCurrencyDdl')
        sleep(1.5)
        select_trc20.click()

        for _ in range(19):
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.2)
        actions.send_keys(Keys.ENTER).perform()
        sleep(0.5)
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    sleep(3)

    try:
        driver.implicitly_wait(10)
        next_step_2 = driver.find_element(By.ID, 'CryptoPopupContinuePaymentButton')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", next_step_2)
    except Exception as e:
        print(f'ERROR NEXT STEP2 \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            sleep(5.5)
            driver.implicitly_wait(60)
            amount = driver.find_element(By.ID, 'CryptoPopupPaymentAmountValue').text

            driver.implicitly_wait(10)
            address = driver.find_element(By.ID, 'CryptoPopupOpenInWalletLink').get_attribute('data-alternative-url')

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
