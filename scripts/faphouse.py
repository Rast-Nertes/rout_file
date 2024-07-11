from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://faphouse.com/ru?returnUrl=https%3A%2F%2Ffaphouse.com%2Fru%2Fjoin%3Fjes%3Dheader#signin'
user_email = "nobrandnametoshow@gmail.com"
user_password = "kiramira123"

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
# options.binary_location = chrome_path

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


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(90)
        input_email = driver.find_element(By.XPATH, '(//input[@name="login"])[1]')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '(//input[@name="password"])[1]')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '(//button[@type="submit"])[1]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    try:
        choose_tariff = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div/div/div/div[3]/div[1]/section/div[1]/div[3]'))
        )
        choose_tariff.click()

        choose_crypto = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//img[@alt="cryptocoin"]'))
        )
        choose_crypto.click()
    except Exception as e:
        print(f'ERROR CHOOSE TARIFF \n{e}')

    try:
        click_accept_but = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/div/div/div/div/div[3]/div[1]/section/button'))
        )
        click_accept_but.click()
    except Exception as e:
        print(f'ERROR ACCEPT CHOOSE \n{e}')

    try:
        sleep(10)
        driver.implicitly_wait(40)
        continue_but = driver.find_element(By.XPATH, '(//button[@type="button"])[5]')
        sleep(2.5)
        # driver.execute_script("arguments[0].click();", continue_but)
        continue_but.click()
    except Exception as e:
        print(f'ERROR CHOOSE USDT \n{e}')

    try:
        choose_tron_net = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//label[@data-test="Tron-currency"]'))
        )
        driver.execute_script("arguments[0].click();", choose_tron_net)

        sleep(5)
        continue_but = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '(//button[@type="button"])[5]'))
        )
        continue_but.click()
    except Exception as e:
        print(f'ERROR CHOOSE NET \n{e}')

    try:
        input_email_step_2 = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//input[@name="email"]'))
        )
        input_email_step_2.send_keys(user_email)

        continue_but = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '(//button[@type="button"])[5]'))
        )
        continue_but.click()
    except Exception as e:
        print(f'error input email \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        sleep(3.5)
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