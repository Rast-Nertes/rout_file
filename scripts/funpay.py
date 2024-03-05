from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://funpay.com/account/login'
user_login = "kiracase34@gmail.com"
user_password = "ZUR/e?+9J!.5E@E"

#API CONSTANS


api_key = '7f728c25edca4f4d0e14512d756d6868'
site_key = '6LdTYk0UAAAAAGgiIwCu8pB3LveQ1TcLUPXBpjDh'

def solver_captcha(api_key, url, site_key):
    from twocaptcha import TwoCaptcha
    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
            sitekey=site_key,
            url=url
        )
        return result['code']
    except Exception as e:
        print(f"CAPTCHA ERROR \n{e}")
        result = "None"
    print(result)
    return result

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

def login(driver):
    driver.maximize_window()
    driver.get(url)

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.CSS_SELECTOR, 'div > form > div:nth-child(3) > input:nth-child(2)')
        input_email.clear()
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'div > form > div:nth-child(3) > input.form-control.mt10')
        input_password.clear()
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    result_captcha = solver_captcha(api_key, url, site_key)
    if result_captcha == 'None':
        result_captcha = solver_captcha(api_key, url, site_key)
    print(result_captcha)
    try:
        driver.implicitly_wait(20)
        input_result_captcha = driver.find_element(By.ID, 'g-recaptcha-response')
        driver.execute_script("arguments[0].style.display = 'block';", input_result_captcha)

        input_result_captcha.clear()
        input_result_captcha.send_keys(result_captcha)
        sleep(3)
    except Exception as e:
        print(f"ERROR CAPTCHA INPUT \n{e}")

    try:
        driver.implicitly_wait(10)
        button_login_click = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div > form > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", button_login_click)
    except Exception as e:
        print(f"BUTTON ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        actions = ActionChains(driver)
        login(driver)
        sleep(3)
        driver.refresh()
        sleep(2)
        driver.get('https://funpay.com/en/lots/offer?id=24639037')

        # try:
        #     driver.implicitly_wait(20)
        #     add_funds = driver.find_element(By.CSS_SELECTOR, '#content > div > div > div:nth-child(3) > a')
        #     sleep(1.5)
        #     driver.execute_script("arguments[0].click();", add_funds)
        # except Exception as e:
        #     print(f"ADD FUNDS ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_method = driver.find_element(By.CSS_SELECTOR, 'div.col-md-5.col-sm-9 > div > div.param-list > form > div:nth-child(5) > div > button > div')
            sleep(1.5)
            choose_method.click()

            for _ in range(5):
                actions.send_keys(Keys.ARROW_DOWN).perform()
                sleep(0.5)

            actions.send_keys(Keys.ENTER).perform()
        except Exception as e:
            print(f"CHOOSE METHOD ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            buy_button = driver.find_element(By.CSS_SELECTOR, 'div > div.col-md-5.col-sm-9 > div > div.param-list > form > div:nth-child(8) > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_button)
        except Exception as e:
            print(f"BUY BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            pay_button = driver.find_element(By.CSS_SELECTOR, 'div > div.col-lg-3.col-md-4.col-sm-9.col-md-offset-0.col-sm-offset-3 > div > form > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", pay_button)
        except Exception as e:
            print(f"PAY BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            address = driver.find_element(By.CSS_SELECTOR, 'div > div.row > div.col-lg-5.col-sm-7.col-lg-pull-7.col-sm-pull-5 > div:nth-child(1) > div > input').get_attribute('value')

            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, 'div > div.row > div.col-lg-5.col-sm-7.col-lg-pull-7.col-sm-pull-5 > div:nth-child(2) > div > input').get_attribute('value')

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
