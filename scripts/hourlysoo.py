from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.imagecaptcha import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://hourlysoo.com/?a=login'
user_email = "kiracase34"
user_password = "wyD37QVnCRweg8h"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

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


def captcha_solver():
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key("6ab87383c97cb688c42b47e81c96bbcc")

    captcha_text = solver.solve_and_return_solution("captcha.jpg")
    time.sleep(1)

    if captcha_text != 0:
        print("captcha text " + captcha_text)
    else:
        print("task finished with error " + solver.error_code)

    return captcha_text


def login(driver):
    driver.get(url)
    driver.maximize_window()

    driver.set_window_size(400, 400)
    driver.execute_script("document.body.style.zoom='300%'")
    driver.execute_script("window.scrollBy(520, 1570);")

    sleep(3)
    driver.save_screenshot("captcha.jpg")
    result = captcha_solver()

    driver.maximize_window()
    driver.execute_script("document.body.style.zoom='100%'")

    try:
        driver.implicitly_wait(10)
        input_captcha = driver.find_element(By.CSS_SELECTOR, 'div.hero > div.container > div > div.col-lg-10.col-xl-8 > div > div > form > div:nth-child(8) > div > input')
        input_captcha.clear()
        input_captcha.send_keys(result)
    except Exception as e:
        print(f"ERROR INPUT CAPTCHA \n{e}")

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.CSS_SELECTOR, 'div > div.col-lg-10.col-xl-8 > div > div > form > div:nth-child(6) > div > input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'div > div.col-lg-10.col-xl-8 > div > div > form > div:nth-child(7) > input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'div.container > div > div.col-lg-10.col-xl-8 > div > div > form > div.d-flex.align-items-center.pt-2 > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    try:
        driver.implicitly_wait(5)
        find_error = driver.find_element(By.CSS_SELECTOR, 'div.container > div > div.col-lg-10.col-xl-8 > div > div > div.error').text

        if "wrong" in find_error:
            driver.set_window_size(400, 400)
            driver.execute_script("document.body.style.zoom='300%'")
            driver.execute_script("window.scrollBy(540, 1570);")

            sleep(4)
            driver.save_screenshot("captcha.jpg")
            result = captcha_solver()

            driver.maximize_window()
            driver.execute_script("document.body.style.zoom='100%'")

            try:
                driver.implicitly_wait(10)
                input_captcha = driver.find_element(By.CSS_SELECTOR, 'div.hero > div.container > div > div.col-lg-10.col-xl-8 > div > div > form > div:nth-child(8) > div > input')
                input_captcha.clear()
                input_captcha.send_keys(result)
            except Exception as e:
                print(f"ERROR INPUT CAPTCHA \n{e}")

            try:
                driver.implicitly_wait(30)
                input_email = driver.find_element(By.CSS_SELECTOR, 'div > div.col-lg-10.col-xl-8 > div > div > form > div:nth-child(6) > div > input')
                input_email.clear()
                input_email.send_keys(user_email)

                driver.implicitly_wait(10)
                input_password = driver.find_element(By.CSS_SELECTOR, 'div > div.col-lg-10.col-xl-8 > div > div > form > div:nth-child(7) > input')
                input_password.clear()
                input_password.send_keys(user_password)

                driver.implicitly_wait(10)
                login_button = driver.find_element(By.CSS_SELECTOR, 'div.container > div > div.col-lg-10.col-xl-8 > div > div > form > div.d-flex.align-items-center.pt-2 > button')
                sleep(1.5)
                driver.execute_script("arguments[0].click();", login_button)
            except Exception as e:
                print(f"LOGIN ERROR \n{e}")
    except:
        pass
    sleep(2)
    driver.get('https://hourlysoo.com/?a=deposit')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        actions = ActionChains(driver)
        login(driver)

        try:
            driver.implicitly_wait(10)
            select_plan = driver.find_element(By.CSS_SELECTOR, 'div.dashboard__content > form > div.row > div > div > div > div:nth-child(1) > div > div:nth-child(1) > div > div > div.faq-list__a.p-0.pt-5 > div > select')
            sleep(1.5)
            select_plan.click()
        except Exception as e:
            print(f"ERROR SELECT \n{e}")

        actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()
        sleep(0.5)
        try:
            driver.implicitly_wait(10)
            input_amount = driver.find_element(By.CSS_SELECTOR, 'form > div.row > div > div > div > div:nth-child(1) > div > div:nth-child(2) > div > div > div.faq-list__a.p-0.pt-5 > div.form-group.col-xl-9.mb-5 > input.form-control.calc__amount.mb-0')
            input_amount.clear()
            input_amount.send_keys('30')

            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.ID, 'deposit--process--92')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(10)
            submit_button = driver.find_element(By.CSS_SELECTOR, 'div.dashboard__main > div.dashboard__content > form > div.row > div > div > div > div:nth-child(1) > div > div:nth-child(3) > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit_button)
        except Exception as e:
            print(f"SUBMIT BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            process_button = driver.find_element(By.CSS_SELECTOR, 'form > span.deposit-process-wrap > input')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", process_button)
        except Exception as e:
            print(f"ERROR PROCESS BUTTON \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_trc20_step2 = driver.find_element(By.CSS_SELECTOR, '#coin_select > div.list-group.mt-2.list > div:nth-child(22) > label')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20_step2)

            driver.implicitly_wait(10)
            pay_button = driver.find_element(By.ID, 'dbtnCheckout')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", pay_button)
        except Exception as e:
            print(f"PAY ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[1]/form/div[2]/div[1]/div[3]/div[2]').text

            driver.implicitly_wait(10)
            amount = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[1]/form/div[2]/div[1]/div[1]/div[2]').text.replace("USDT.TRC20", '').replace(" ", '')

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
