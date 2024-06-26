from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://recon-zone.ru/checkout/?add-to-cart=7542'
user_email = "rwork875@gmail.com"
user_password = "1122334455Rwork"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


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
        click(driver, 30, '//a[@class="e-show-login"]')
    except Exception as e:
        print(f'ERROR LOG BUT \n{e}')

    try:
        input_data(driver, 30, '//*[@id="username"]', user_email)
        input_data(driver, 30, '//*[@id="password"]', user_password)
        click(driver, 30, '//button[@class="woocommerce-button button woocommerce-form-login__submit e-woocommerce-form-login-submit"]')

        sleep(5)

        click(driver, 30, '//*[@id="payment_method_cryptocloud"]')
        click(driver, 30, '//*[@id="terms"]')
        click(driver, 30, '//*[@id="place_order"]')
    except Exception as e:
        print(f'ERROR MAKE ACTIONS \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        log = login(driver)
        if log:
            return log

        try:
            sleep(2.5)
            driver.implicitly_wait(25)
            amount = driver.find_element(By.XPATH,
                                         '//*[@id="app"]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/span').text.replace(
                "USDT", '').replace(" ", '')

            driver.implicitly_wait(20)
            address = driver.find_element(By.XPATH,
                                          '//*[@id="app"]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div/span').text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:

            try:
                click(driver, 20, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[3]/button')
            except Exception as e:
                print(f'ERROR NEXT BUT \n{e}')

            try:
                sleep(2.5)
                driver.implicitly_wait(65)
                amount = driver.find_element(By.XPATH,
                                             '//*[@id="app"]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/span').text.replace(
                    "USDT", '').replace(" ", '')

                driver.implicitly_wait(20)
                address = driver.find_element(By.XPATH,
                                              '//*[@id="app"]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div/span').text

                return {
                    "address": address,
                    "amount": amount,
                    "currency": "usdt"
                }
            except Exception as e:
                print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
