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

url = 'https://s1.cosmo-games.pro/login'
user_email = "kiracase34@gmail.com"
user_password = "kirakira222"

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
    actions = ActionChains(driver)
    driver.get(url)
    driver.maximize_window()

    try:
        input_data(driver, 25, '//*[@id="log_email"]', user_email)
        sleep(1)
        input_data(driver, 25, '//*[@id="pass"]', user_password)
        sleep(1)
        click(driver, 20, '/html/body/div/div/div[2]/form/button')
    except Exception as e:
        return {"status":"0", "ext":f"error input log data {e}"}

    try:
        click(driver, 20, '/html/body/div[3]/div[2]/div[2]/div[2]/div[1]/div/a')
    except Exception as e:
        return {"status":"0", "ext":f"error add amount {e}"}

    try:
        driver.implicitly_wait(20)
        click_select = driver.find_elements(By.ID, 'add_PSys')
        sleep(1)
        click_select[1].click()

        actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()
        sleep(0.5)
    except Exception as e:
        return {"status":"0", "ext":f"error click {e}"}

    try:
        click(driver, 20, '/html/body/div[3]/div[2]/div/div[2]/form/input[3]')
    except Exception as e:
        return {"status":"0", "ext":f"error append {e}"}

    try:
        input_data(driver, 20, '//*[@id="psevdo"]', 650)
    except Exception as e:
        return {"status":"0", "ext":f"error input data {e}"}

    try:
        click(driver, 20, '//*[@id="submit"]')
    except Exception as e:
        return {"status":"0", "ext":f"error submit {e}"}

    try:
        click(driver, 20, '/html/body/div[3]/div[2]/div/div[2]/center/form/center/input')
    except Exception as e:
        return {"status":"0", "ext":f"error buy silver {e}"}


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
            return {"status":"0", "ext":f"error input email {e}"}

        try:
            driver.implicitly_wait(60)
            submit_payment = driver.find_element(By.ID, 'submit-payment')
            sleep(1.5)
            submit_payment.click()
        except Exception as e:
            return {"status":"0", "ext":f"error submit {e}"}

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
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
