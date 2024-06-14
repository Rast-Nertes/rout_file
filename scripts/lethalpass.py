from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://www.lethalpass.com/join'
user_email = "yewoxo4550@otemdi.com"
user_password = "onvB2mkVH5c"

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
        click(driver, 35, '/html/body/div[1]/div/form/div[2]/div[1]/div/div[1]')
        sleep(1)
        click(driver, 30, '/html/body/div[1]/div/form/div[2]/div[2]/ul/li[3]/div/label')
    except Exception as e:
        print(f'ERROR CHOOSE TARIFF')

    try:
        click(driver, 20, '/html/body/div[1]/div/form/div[2]/div[3]/input')
    except Exception as e:
        print(f'ERROR NEXT BUT \n{e}')

    try:
        click(driver, 35, '//*[@id="coin_label_USDT"]')
        sleep(1)
        click(driver, 20, '//*[@id="wrapper"]/div[1]/div/div[1]/div[5]/fieldset/div/div/div[1]/label[1]')
    except Exception as e:
        print(f'ERROR CHOOSE USDT \n{e}')

    try:
        input_data(driver, 30, '//*[@id="email"]', user_email)
        sleep(1)
        click(driver, 20, '//*[@id="submit"]')
    except Exception as e:
        print(f'ERROR SUBMIT BUTTON \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(5.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[1]').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]').text.replace("USDT", '').replace("TRX", '').replace("\n", '').replace(" ", '')

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
