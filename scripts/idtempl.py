from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://idtempl.com/my-account/'
user_email = "kiracase34@gmail.com"
user_password = "JR9vzh2sDvuTt2@"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

def solve_captcha():
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key("6ab87383c97cb688c42b47e81c96bbcc")
    solver.set_website_url(url)
    solver.set_website_key("6LfmjcAiAAAAAA3IZHNxmhNZX6Ls01dg3RfAhZlK")
    solver.set_soft_id(0)

    g_response = solver.solve_and_return_solution()
    return g_response


def login(driver):
    driver.get(url)
    driver.maximize_window()

    captcha_code = solve_captcha()
    input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
    driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, captcha_code)
    sleep(1.5)

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.CSS_SELECTOR, 'div.xoo-el-section.xoo-el-active > div > form > div.xoo-aff-group.xoo-aff-cont-text.one.xoo-aff-cont-required.xoo-el-username_cont > div > input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'div.xoo-el-section.xoo-el-active > div > form > div.xoo-aff-group.xoo-aff-cont-password.one.xoo-aff-cont-required.xoo-el-password_cont > div > input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'div.xoo-el-form-container.xoo-el-form-inline > div.xoo-el-section.xoo-el-active > div > form > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        while True:
            try:
                driver.implicitly_wait(5)
                find_error = driver.find_element(By.CSS_SELECTOR, 'div.xoo-el-form-container.xoo-el-form-inline > div.xoo-el-section.xoo-el-active > div > div > div > strong').text
                if "Error" in find_error:
                    login(driver)
            except:
                break
                pass

        sleep(2)
        driver.get('https://idtempl.com/product/bangladesh-id-card-psd-template/?swcfpc=1')

        try:
            driver.implicitly_wait(10)
            buy_now_button = driver.find_element(By.CSS_SELECTOR, '#shop-now > button.tbay-buy-now.button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_now_button)

            driver.implicitly_wait(10)
            input_count = driver.find_element(By.XPATH, '/html/body/div[2]/div[4]/section/div/div/div/div/form/div/div[1]/div[1]/div[2]/div[3]/div/span/input')
            input_count.clear()
            input_count.send_keys('1')

            driver.implicitly_wait(10)
            update_cart = driver.find_element(By.CSS_SELECTOR, 'div.cart-bottom.clearfix.actions > div.update-cart.pull-right > input')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", update_cart)
            sleep(5)

            driver.implicitly_wait(10)
            proceed_button = driver.find_element(By.CSS_SELECTOR, 'div > div.col-12.col-xl-4.tb-cart-total > div.wc-proceed-to-checkout > a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", proceed_button)
        except Exception as e:
            print(f"INPUT COUNT ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_zipcode = driver.find_element(By.ID, 'billing_postcode')
            input_zipcode.clear()
            input_zipcode.send_keys("12345")
            sleep(1.5)

            driver.implicitly_wait(10)
            choose_nowpayments = driver.find_element(By.ID, 'payment_method_nowpayments')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_nowpayments)
            sleep(1.5)

            driver.implicitly_wait(10)
            ticket = driver.find_element(By.ID, 'terms')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", ticket)

            driver.implicitly_wait(10)
            place_order = driver.find_element(By.ID, 'place_order')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", place_order)
        except Exception as e:
            print(f"ERROR PLACE ORDER BUTTON \n{e}")

        try:
            driver.implicitly_wait(20)
            next_step_button = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[1]/div[3]/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step_button)
            while True:
                driver.implicitly_wait(5)
                error = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[1]/div[3]/div[3]').text
                if error == None:
                    break
                else:
                    driver.execute_script("arguments[0].click();", next_step_button)
            sleep(3)
        except Exception as e:
            print(f"ERROR NEXT STEP BUTTON \n{e}")

        try:
            driver.implicitly_wait(10)
            amount = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]').text.replace('USDT', '').replace(" ", '').replace('TRX', '').replace('\n', '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR, 'div.send-deposit-step > div.send-deposit-step__body > div.send-deposit-step__info > div:nth-child(2) > div.payment-info-item__content > div > div.copy-text__box').text

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
