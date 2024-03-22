from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.turnstileproxyless import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://sso.adultwork.com/login'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123!"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

def captcha_solver():
    solver = turnstileProxyless()
    solver.set_verbose(1)
    solver.set_key("6ab87383c97cb688c42b47e81c96bbcc")
    solver.set_website_url("https://sso.adultwork.com/login")
    solver.set_website_key("0x4AAAAAAADhZLig6qEG5LvP")
    solver.set_soft_id(0)

    token = solver.solve_and_return_solution()
    return token


def login(driver):
    driver.get(url)
    driver.maximize_window()
    sleep(10)

    try:
        driver.implicitly_wait(20)
        input_data = driver.find_element(By.XPATH, '/html/body/div/main/section/div/div/div/form/div[3]/input')
        sleep(1.5)
        driver.execute_script("arguments[0].removeAttribute('type');", input_data)

        try:
            driver.implicitly_wait(10)
            remove_attribute_button = driver.find_element(By.ID, 'submit')
            driver.execute_script("arguments[0].removeAttribute('disabled');", remove_attribute_button)
        except Exception as e:
            print(f"ERROR REMOVE \n{e}")

        result_captcha = captcha_solver()
        input_data.send_keys(result_captcha)
    except Exception as e:
        print(f"ERROR REMOVE STYLE \n{e}")

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.ID, 'nickname')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.ID, 'password')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.ID, 'submit')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        actions = ActionChains(driver)
        login(driver)

        try:
            driver.implicitly_wait(10)
            continue_button = driver.find_element(By.CSS_SELECTOR, 'div > center > table > tbody > tr:nth-child(6) > td:nth-child(1) > a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button)
        except Exception as e:
            print(f"ERROR CONTINUE BUTTON \n{e}")

        sleep(3)
        # driver.get('https://adultwork.com/dlgBuyCredits.asp')
        driver.get('https://m.adultwork.com/payments')
        # try:
        #     driver.implicitly_wait(30)
        #     select_method = driver.find_element(By.CSS_SELECTOR, 'form > table > tbody > tr > td:nth-child(2) > select')
        #     sleep(1.5)
        #     select_method.click()
        #
        #     for _ in range(5):
        #         actions.send_keys(Keys.ARROW_DOWN).perform()
        #         sleep(0.5)
        #
        #     actions.send_keys(Keys.ENTER).perform()
        #
        #     driver.implicitly_wait(10)
        #     buy_now_button = driver.find_element(By.CSS_SELECTOR, 'tbody > tr:nth-child(2) > td > input')
        #     sleep(1.5)
        #     driver.execute_script("arguments[0].click();", buy_now_button)
        # except Exception as e:
        #     print(f"ERROR CHOOSE BIT PAYMENT \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_crypto_pay = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div/div[2]/label[4]/div/div[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_crypto_pay)

            driver.implicitly_wait(10)
            input_amount = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div/div[3]/div[2]/label[5]/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", input_amount)

            driver.implicitly_wait(10)
            continue_button_2 = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/div[2]/div/div[3]/div[5]/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button_2)
        except Exception as e:
            print(f"ERROR CHOOSE METHOD \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_usdt = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div/label[8]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_usdt)

            driver.implicitly_wait(10)
            continue_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button)
        except Exception as e:
            print(f"ERROR CHOOSE USDT \n{e}")

        try:
            driver.implicitly_wait(10)
            without_email = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[1]/div[2]/button[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", without_email)

            driver.implicitly_wait(10)
            choose_tron = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[3]/div/div/label[3]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_tron)

            driver.implicitly_wait(10)
            continue_button_2 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div[2]/div/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button_2)
        except Exception as e:
            print(f"ERROR CHOOSE TRON \n{e}")

        driver.set_window_size(1200, 500)

        try:
            driver.implicitly_wait(60)
            amount = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/p').text.replace("USDT", '').replace(" ", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[6]/div/div[2]/div/p').text

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
