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

url = 'https://shop-accounts.com/order-betting-accounts/'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(30)
        choose_dafa_bet = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/main/div/div/div/div/div/form/div[2]/div[1]/div/label[1]/span[2]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", choose_dafa_bet)

        driver.implicitly_wait(40)
        ticket = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/main/div/div/div/div/div/form/div[4]/div[2]/div/label[2]/span[2]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", ticket)
    except Exception as e:
        return {"status":"0", "ext":f"error actions {e}"}

    try:
        driver.implicitly_wait(30)
        input_tranc = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/main/div/div/div/div/div/form/div[6]/div/div/input')
        input_tranc.send_keys("111111")

        driver.implicitly_wait(30)
        input_email = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/main/div/div/div/div/div/form/div[7]/div[1]/div/input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(20)
        ticket_2 = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/main/div/div/div/div/div/form/div[7]/div[2]/div/div/label')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", ticket_2)
    except Exception as e:
        return {"status":"0", "ext":f"error some data{e}"}

    try:
        driver.implicitly_wait(30)
        submit_button = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/main/div/div/div/div/div/form/div[8]/div/div/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", submit_button)
    except Exception as e:
        return {"status":"0", "ext":f"error submit {e}"}


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(50)
            address = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/main/div/div/div/div/div/form/div[1]/div/table/tbody/tr/td/ul[3]/li').text

            driver.implicitly_wait(10)
            amount = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/main/div/div/div/div/div/form/div[1]/div/table/tbody/tr/td/p[1]/b').text.replace("$", '').replace(" ", '')

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