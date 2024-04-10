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

url = 'https://betlab.club/login'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

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
        input_data(driver, 35, '/html/body/div/div[2]/div/form/label[1]/input', user_email)
        sleep(1)
        input_data(driver, 20, '/html/body/div/div[2]/div/form/label[2]/input', user_password)
        sleep(1)
        click(driver, 20, '/html/body/div/div[2]/div/form/div[1]/label[1]')
    except Exception as e:
        print(f"ERROR LOGIN \n{e}")

    sleep(3.5)
    driver.get('https://betlab.club/plans')

    try:
        click(driver, 20, '/html/body/div[1]/div[2]/div/div[3]/div[1]/div[2]/div/form/div/button')
        sleep(1)
        click(driver, 20, '/html/body/div[4]/div[1]/div[2]/div[2]/div[2]/button[2]')
        sleep(1)
        click(driver, 20, '/html/body/div[4]/div[1]/button')
        sleep(1)
        click(driver, 20, '/html/body/div[4]/div[1]/div[3]/button[2]')
    except Exception as e:
        print(f"ERROR INPUT AMOUNT \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div/div/div[1]/div[6]/div[1]').text

            driver.implicitly_wait(20)
            amount_text = driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div/div/div[1]/div[2]/div').text
            amount_index = amount_text.find('$')
            amount = amount_text[amount_index + 1:]

            return {
                "address": address,
                "amount": amount + '.00',
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
