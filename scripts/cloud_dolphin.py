from time import sleep
from flask import Flask, jsonify
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://cloud.dolphin.tech/ru/#tariffs'
user_login = 'kiracase34@gmail.com'
user_password = 'w!U7yPGeh5FfUx5'

#PROXY_CONSTANS

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

#CHROME OPTIONS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        button_to_log = driver.find_element(By.XPATH, '//a[@class="nav__login"]')
        sleep(1)
        driver.execute_script("arguments[0].click();", button_to_log)
    except Exception as e:
        print(f"BUTTON ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.ID, 'email-form')
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.ID, 'password-field')
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        click_button_to_log = driver.find_element(By.CSS_SELECTOR, '#login > button')
        driver.execute_script("arguments[0].click();", click_button_to_log)
    except Exception as e:
        print(f"CLICK BUTTON ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        sleep(5)
        driver.get('https://cloud.dolphin.tech/app/fb/profile/tariffs')

        try:
            driver.implicitly_wait(30)
            choose_tariff = driver.find_element(By.XPATH, '(//button[@class="choose-plan-btn"])[4]')
            sleep(1)
            driver.execute_script("arguments[0].click();", choose_tariff)
        except Exception as e:
            print(f"CHOOSE TARIFF \n{e}")

        try:
            driver.implicitly_wait(20)
            choose_payment_method = driver.find_element(By.CSS_SELECTOR, 'div.crypto-payments-container > div.cryptadium-payment-item.payment-item0')
            driver.execute_script("arguments[0].click();", choose_payment_method)
        except Exception as e:
            print(f"CHOOSE PAYMENT METHOD ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            buy_button = driver.find_element(By.CSS_SELECTOR, 'div.to-pay-container > div.datas-block-container > button > span')
            driver.execute_script("arguments[0].click();", buy_button)
        except Exception as e:
            print(f"BUT BUTTON ERROR \n{e}")

        sleep(10)
        new_window = driver.window_handles[-1]
        driver.switch_to.window(new_window)

        try:
            driver.implicitly_wait(10)
            next_step_to_payment = driver.find_element(By.CSS_SELECTOR, '#redirectButton')
            sleep(2)
            driver.execute_script("arguments[0].click();", next_step_to_payment)
        except:
                sleep(2)
                driver.implicitly_wait(10)
                address = driver.find_element(By.XPATH,
                                              '//*[@id="payment-form"]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/p').text

                driver.implicitly_wait(10)
                amount = driver.find_element(By.XPATH,
                                             '//*[@id="payment-form"]/div/div[2]/div[1]/div[1]/div[2]/div/div[2]/div[2]/p').text

                return {
                    "address": address,
                    "amount": amount,
                    "currency": "usdt"
                }
        try:
            driver.implicitly_wait(20)
            address = driver.find_element(By.CSS_SELECTOR,
                                          'div.payment_requisites > div.req_to_clipboard_wrapper > div > p').text

            driver.implicitly_wait(10)
            amount = driver.find_element(By.CSS_SELECTOR,
                                         'div.payment_req > div > div.payment_requisites > div.req_to_clipboard > p').text

            return {
                "address": amount,
                "amount": address,
                "currency": "usdt"
            }

        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
