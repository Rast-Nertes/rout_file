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

url = 'https://s1.fruit-tree.ink/login'
user_email = "kiracase34@gmail.com"
user_password = "E9nvJLtnYzSr296"

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
        input_data(driver, 35, '/html/body/div/div/div[2]/form/input[1]', user_email)
        sleep(1)
        input_data(driver, 20, '/html/body/div/div/div[2]/form/input[2]', user_password)
        sleep(1)
        click(driver, 20 ,'/html/body/div/div/div[2]/form/span/input')
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    try:
        click(driver, 20, '/html/body/div[3]/div[2]/div/div[2]/a')
    except Exception as e:
        print(f"error next step \n{e}")

    try:
        driver.implicitly_wait(20)
        click_fre = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[2]/b/div/div[2]')
        sleep(2.5)
        click_fre.click()
    except Exception as e:
        print(f'ERROR CHOOSE FREKASSA \n{e}')

    try:
        input_data(driver, 30, '//*[@id="psevdo"]', '650')
        sleep(1)
        click(driver, 20, '/html/body/div[3]/div[3]/b/form/input[4]')
    except Exception as e:
        print(f'ERROR INPUT AMOUNT \n{e}')

    try:
        click(driver, 20, '/html/body/div[3]/div[3]/b/center/form/input[8]')
    except Exception as e:
        print(f'ERROR NEXT \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(60)
            choose_trc20 = driver.find_element(By.ID, 'currency-15')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(40)
            input_email = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[1]/div/form/div/div[2]/input')
            input_email.clear()
            input_email.send_keys(user_email)
        except Exception as e:
            print(f"INPUT EMAIL \n{e}")

        try:
            driver.implicitly_wait(60)
            submit_payment = driver.find_element(By.ID, 'submit-payment')
            sleep(1.5)
            submit_payment.click()
        except Exception as e:
            print(f"SUBMIT ERROR \n{e}")

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[7]/div[2]').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[5]/span').text

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
