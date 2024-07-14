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


with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    ext = paths[1].strip()

options.add_extension(ext)


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    elem_click.click()


def js_click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    driver.execute_script("arguments[0].click();", elem_click)


def wait_visibility(driver, time, XPATH):
    WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.XPATH, XPATH))
    )
    sleep(2.5)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


def api_connect(driver):
    sleep(1.5)
    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        sleep(1.5)
        if "2Cap" in driver.title:
            break

    try:
        js_click(driver, 30, '//*[@id="autoSolveRecaptchaV2"]')
        js_click(driver, 30, '//*[@id="autoSolveInvisibleRecaptchaV2"]')
        js_click(driver, 30, '//*[@id="autoSolveRecaptchaV3"]')
        js_click(driver, 30, '//*[@id="autoSolveHCaptcha"]')

        input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        click(driver, 30, '//*[@id="connect"]')
        sleep(4.5)
        driver.switch_to.alert.accept()
    except Exception as e:
        print(f'ERROR CLICK \n{e}')

    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        sleep(1.5)
        if not("2Cap" in driver.title):
            break


def login(driver):
    api_connect(driver)
    driver.get(url)
    driver.maximize_window()

    try:
        input_data(driver, 15, '(//form/div/div/div/input)[1]', user_email)
        input_data(driver, 10, '(//form/div/div/div/input)[2]', user_password)
    except Exception as e:
        print(f'ERROR INPUT LOG DATA \n{e}')

    try:
        time_loop = 0
        while True:
            driver.implicitly_wait(10)
            find_check = driver.find_element(By.XPATH, '//div[@class="captcha-solver-info"]').text
            if ("ена" in find_check) or ("lve" in find_check):
                break
            else:
                if time_loop > 120:
                    return {"status": "0", "ext": "CAPTCHA ERROR"}
                time_loop += 5
                sleep(5)
                print("Wait 5 seconds, captcha solving...")
    except Exception as e:
        print(f'ERROR CHECKBOX ')

    try:
        click(driver, 10, '(//button[@type="submit"])[2]')
    except Exception as e:
        print(f'ERROR CLICK LOG BUT \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        sleep(7.5)
        driver.get('https://idtempl.com/product/bangladesh-id-card-psd-template/?swcfpc=1')

        try:
            driver.implicitly_wait(10)
            buy_now_button = driver.find_element(By.CSS_SELECTOR, '#shop-now > button.tbay-buy-now.button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_now_button)
        except Exception as e:
            print(f'ERROR BUY BUT \n{e}')

        sleep(1.5)

        try:
            driver.implicitly_wait(10)
            input_count = driver.find_element(By.XPATH, '/html/body/div[2]/div[4]/section/div/div/div/div/form/div/div[1]/div[1]/div[2]/div[3]/div/span/input')
            input_count.clear()
            input_count.send_keys('1')
        except Exception as e:
            print(f'ERROR INPUT COUNT \n{e}')

        try:
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
            print(f"UPDATE CART ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_zipcode = driver.find_element(By.ID, 'billing_postcode')
            input_zipcode.clear()
            input_zipcode.send_keys("12345")
            sleep(1.5)

            # driver.implicitly_wait(10)
            # choose_nowpayments = driver.find_element(By.ID, 'payment_method_nowpayments')
            # sleep(1.5)
            # driver.execute_script("arguments[0].click();", choose_nowpayments)

            sleep(7.5)

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
