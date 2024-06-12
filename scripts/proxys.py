from anticaptchaofficial.imagecaptcha import *
from seleniumwire import webdriver
from time import sleep
from flask import Flask, jsonify
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


#CONSTANS

user_login = 'kiracase34@gmail.com'
user_password = 'qnCH7mNd'
url = 'https://proxys.io/ru/user/login'

#PROXY_CONSTANS

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@196.19.121.187:8000",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")


with open('config.txt') as file:
    paths = file.readlines()
    api_key = paths[2].strip()


def captcha():
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(api_key)
    solver.set_soft_id(0)

    captcha_text = solver.solve_and_return_solution("captcha.jpeg")
    return captcha_text

def captcha_and_login(driver):
    driver.get(url)

    try:
        input_email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="login-form-login"]'))
        )
        input_email.send_keys(user_login)

        input_password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="login-form-password"]'))
        )
        input_password.send_keys(user_password)

    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    while True:
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="login-form-captcha-image"]'))
            )
            driver.find_element(By.XPATH, '//*[@id="login-form-captcha-image"]').screenshot("captcha.jpeg")
            result = captcha()

            driver.implicitly_wait(5)
            input_captcha = driver.find_element(By.XPATH, '//*[@id="login-form-captcha"]')
            input_captcha.clear()
            input_captcha.send_keys(result)

            driver.implicitly_wait(5)
            click_auth = driver.find_element(By.XPATH, '//button[@type="submit"]')
            click_auth.click()
            sleep(5)
        except Exception as e:
            print(f'Success ')
            break


def get_wallet():
    with webdriver.Chrome(options= options, seleniumwire_options=proxy_options) as driver:
        captcha_and_login(driver)
        driver.get('https://proxys.io/ru/cart')
        actions = ActionChains(driver)
        try:
            ind_ipv4 = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="accordion"]/div[1]/div[1]'))
            )
            ind_ipv4.click()
            #Время для анимации
            sleep(2)

            driver.execute_script("window.scrollBy(0, 100);")
        except Exception as e:
            print(f'IPv4 ERROR \n{e}')

        try:
            select_county = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="ip4paymentform-country"]'))
            )
            select_county.click()

            actions.send_keys(Keys.ARROW_DOWN).perform()
            actions.send_keys(Keys.ENTER).perform()
        except Exception as e:
            print(f"COUNTRY ERROR \n{e}")

        try:
            ticket = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="ip4paymentform-terms"]'))
            )
            ticket.click()
        except Exception as e:
            print(f'TICKET ERROR\n{e}')

        try:
            choose_crypto_currency = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="ip4-payment-form"]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/span/span[1]/span'))
            )
            choose_crypto_currency.click()

            sleep(1)

            actions.send_keys(Keys.ARROW_DOWN).perform()
            actions.send_keys(Keys.ENTER).perform()
        except Exception as e:
            print(f"CHOOSE CRYPTO CURRENCY ERROR\n{e}")

        try:
            continue_payment = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="ip4-payment-form"]/div/div[2]/div/div/div[2]/div[2]/button'))
            )
            continue_payment.click()
        except Exception as e:
            print(f'CONTINUE BUTTON ERROR\n{e}')

        try:
            driver.implicitly_wait(10)
            choose_currency = driver.find_element(By.XPATH, '//*[@id="createForm"]/section/div/div[2]/div[1]/ul/li[2]/label')
            driver.execute_script("arguments[0].click();", choose_currency)

            driver.implicitly_wait(10)
            select_network = driver.find_element(By.XPATH, '//input[@type="submit"]')
            driver.execute_script("arguments[0].click();", select_network)
        except Exception as e:
            print(f'CHOOSE USDT ERROR\n{e}')

        try:
            driver.implicitly_wait(10)
            select_net = driver.find_element(By.XPATH, '(//input[@type="submit"])[2]')
            driver.execute_script("arguments[0].click();", select_net)
        except Exception as e:
            print(f"CHOOSE TRC20 \n{e}")

        amount = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="content"]/div/div/section/div/div/div/div[2]/div[6]/div[2]/p'))
        )
        amount = amount.text.replace("USDT", "")

        address = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="content"]/div/div/section/div/div/div/div[2]/div[6]/div[1]/p'))
        )
        address = address.text

        return {
            "address": address,
            "amount": amount.replace(" ", ''),
            "currency": "usdt"
        }


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
