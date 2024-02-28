from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from anticaptchaofficial.hcaptchaproxyless import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://bil.shara.club'
user_login = "kiracase34"
user_password = "gh8ry8TtFiEnZR"

#API CONSTANS

api_key_2captcha = '7f728c25edca4f4d0e14512d756d6868'
api_anticaptcha = '6ab87383c97cb688c42b47e81c96bbcc'
sitekey = '79e5558d-d8bf-4eaf-8014-91f69d0e235d'

def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.CSS_SELECTOR, 'form > table > tbody > tr:nth-child(1) > td:nth-child(2) > input')
        sleep(1.5)
        input_email.clear()
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'form > table > tbody > tr:nth-child(2) > td:nth-child(2) > input')
        sleep(1.5)
        input_password.clear()
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        remove_style_textarea_1 = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/form/table/tbody/tr[3]/td/div/textarea[1]')
        sleep(1.5)
        driver.execute_script("arguments[0].removeAttribute('style');", remove_style_textarea_1)

        driver.implicitly_wait(10)
        remove_style_textarea_2 = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/form/table/tbody/tr[3]/td/div/textarea[2]')
        sleep(1.5)
        driver.execute_script("arguments[0].removeAttribute('style');", remove_style_textarea_2)
    except Exception as e:
        print(f"REMOVE ERROR \n{e}")

    solver = hCaptchaProxyless()
    solver.set_verbose(1)
    solver.set_key(api_anticaptcha)
    solver.set_website_url(url)
    solver.set_website_key(sitekey)

    g_response = solver.solve_and_return_solution()

    if g_response != 0:
        print ("g-response: " + g_response)
    else:
        print("task finished with error " + solver.error_code)
        solver = hCaptchaProxyless()
        solver.set_verbose(1)
        solver.set_key(api_anticaptcha)
        solver.set_website_url(url)
        solver.set_website_key(sitekey)

        g_response = solver.solve_and_return_solution()

    try:
        driver.implicitly_wait(10)
        input_result_capthca = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/form/table/tbody/tr[3]/td/div/textarea[1]')
        sleep(1.5)
        input_result_capthca.clear()
        input_result_capthca.send_keys(g_response)

        driver.implicitly_wait(10)
        input_result_capthca = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/form/table/tbody/tr[3]/td/div/textarea[2]')
        sleep(1.5)
        input_result_capthca.clear()
        input_result_capthca.send_keys(g_response)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        button_login = driver.find_element(By.CSS_SELECTOR, 'form > table > tbody > tr:nth-child(4) > td > input.form-module-button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", button_login)
    except Exception as e:
        print(f"BUTTON LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome() as driver:
        login(driver)
        driver.get('https://bil.shara.club/money.html')

        try:
            driver.implicitly_wait(30)
            choose_cryptocurrency = driver.find_element(By.CSS_SELECTOR, '#tablist > ul > li:nth-child(3) > a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_cryptocurrency)

            driver.implicitly_wait(10)
            input_cash = driver.find_element(By.CSS_SELECTOR, '#tab-17 > div.contentL > form > input[type=text]:nth-child(1)')
            sleep(1.5)
            input_cash.clear()
            input_cash.send_keys("100")

            driver.implicitly_wait(10)
            choose_cryptocloud = driver.find_element(By.CSS_SELECTOR, '#tab-17 > div.contentL > form > button:nth-child(11)')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_cryptocloud)
        except Exception as e:
            print(f"CHOOSE CURRENCY ERROR \n{e}")

        try:
            driver.implicitly_wait(30)
            buy_with_trc_20 = driver.find_element(By.CSS_SELECTOR, 'div.total.col-span-12.md\:col-span-6.lg\:col-span-4.hidden.md\:block.dark\:bg-dark-layout > div.total__footer.border-dot.dark\:bg-dark-layout > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_with_trc_20)

            driver.implicitly_wait(10)
            buy_with_trc = driver.find_element(By.CSS_SELECTOR, 'div.total.col-span-12.md\:col-span-6.lg\:col-span-4.hidden.md\:block.dark\:bg-dark-layout > div.total__footer.border-dot.dark\:bg-dark-layout > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_with_trc)
        except Exception as e:
            print(f"BUY WITH TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(30)
            address = driver.find_element(By.CSS_SELECTOR, 'div.col-span-9.ms-16 > div > div.data-info.pt-12 > div.data-info__address.flex.items-center.justify-between > div > span').text
            driver.implicitly_wait(30)
            amount = driver.find_element(By.CSS_SELECTOR, 'div.total.col-span-12.md\:col-span-6.lg\:col-span-4.hidden.md\:block.dark\:bg-dark-layout > div.total__footer.border-dot.dark\:bg-dark-layout > div:nth-child(1) > span:nth-child(2)').text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }

        except Exception as e:
            print(f"DATA ERROR \n{e}")
            return None


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
