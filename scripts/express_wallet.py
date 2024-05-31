from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.imagecaptcha import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://a96a.express-wallet.info/?a=auth'
user_email = "kiracase34@gmail.com"
user_password = "kiramira555"

with open('config.txt') as file:
    paths = file.readlines()
    api_key = paths[2].strip()


# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def captcha_solver(key):
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(key)

    captcha_text = solver.solve_and_return_solution("captcha.jpg")
    sleep(1)

    if captcha_text != 0:
        print("captcha text " + captcha_text)
    else:
        print("task finished with error " + solver.error_code)

    return captcha_text


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
    # driver.get(url)
    driver.maximize_window()
    #
    # try:
    #     click(driver, 20, '/html/body/div[4]/div[2]/a[2]')
    # except:
    #     pass
    #
    # try:
    #     input_data(driver, 20, '//*[@id="email"]', user_email)
    #     sleep(1)
    #     input_data(driver, 20, '//*[@id="passw"]', user_password)
    # except Exception as e:
    #     print(f'ERROR INPUT \n{e}')
    #
    # driver.find_element(By.XPATH, '//*[@id="reg_cap"]').screenshot('captcha.jpg')
    # sleep(1)
    # result_captcha = captcha_solver(api_key)
    #
    # try:
    #     driver.implicitly_wait(15)
    #     input_captcha = driver.find_element(By.ID, 'capt')
    #     input_captcha.clear()
    #     input_captcha.send_keys(result_captcha)
    #
    # except Exception as e:
    #     print(f'ERROR INPUT CAPTCHA \n{e}')
    #
    # try:
    #     click(driver, 20, '//*[@id="btns"]')
    # except Exception as e:
    #     print(f'ERROR CLICK \n{e}')
    driver.get('https://42c8.express-wallet.site/?a=deposit&umail=kiracase34@gmail.com&hash=a64d63a649b484acde7f1862aa7744fe')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            input_data(driver, 25, '(//*[@id="pay"]/div/input)[1]', "650")
            sleep(1)
            click(driver, 20, '(//*[@id="pay"]/input[2])[1]')
            click(driver, 10, '//input[@name="pay"]')
        except Exception as e:
            return {"status":"0", "ext":f"error inout email {e}"}

        try:
            driver.implicitly_wait(60)
            choose_trc20 = driver.find_element(By.XPATH, '(//*[@id="currency-15"])[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            return {"status":"0", "ext":f"error input email {e}"}

        try:
            driver.implicitly_wait(60)
            submit_payment = driver.find_element(By.ID, 'submit-payment')
            sleep(1.5)
            submit_payment.click()
        except Exception as e:
            return {"status":"0", "ext":f"error submit button  {e}"}

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
