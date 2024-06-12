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

url = 'https://fierrohack.ru'
user_email = "yewoxo4550@otemdi.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS


options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


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
        click(driver, 20, '//*[@id="item-1"]')
    except Exception as e:
        print(f'ERROR CHOOSE ITEM \n{e}')

    try:
        input_data(driver, 20, '//*[@id="input-mail"]', user_email)
        sleep(1)
        click(driver, 20, '//*[@id="buy-button"]')
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    try:
        click(driver, 20, '(//div[@class="payment-method-block"])[7]')
    except Exception as e:
        print(f'ERROR CHOOSE HYPER \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(2.5)
            driver.implicitly_wait(15)
            amount = driver.find_element(By.XPATH,
                                         '//*[@id="app"]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/span').text.replace(
                "USDT", '').replace(" ", '')

            driver.implicitly_wait(10)
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
                amount = driver.find_element(By.XPATH, '//div[@class="amount-clipboard flex items-center"]/span').text.replace("USDT", '').replace(" ", '')

                driver.implicitly_wait(20)
                address = driver.find_element(By.XPATH,'(//div[@class="address-clipboard flex items-center"])[1]/span').text

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
