from selenium import webdriver
from time import sleep
from twocaptcha import TwoCaptcha
from flask import jsonify
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#NOWPAYMENTS

#CONSTANS
user_login = 'kiramira123'
user_password = 'kiramira1'
url = 'https://www.seoclerk.com/login'
site_key = '6Le1vBMTAAAAAIJzghoHt4Rx99unArJikrCvt-Sn'

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()


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
        input_data(driver, 50, '//*[@id="l_username"]', user_login)
        input_data(driver, 30, '//*[@id="l_password"]', user_password)
    except Exception as e:
        print(f"ERROR INPUT DATA \n{e}")

    solver = TwoCaptcha(api_key)

    print("Start solve captcha...")

    result = solver.recaptcha(sitekey=site_key, url=url)
    print(f"РЕЗУЛЬТАТ: {str(result['code'])}")

    driver.implicitly_wait(4.5)
    input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
    driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result['code'])

    try:
        click(driver, 30, '//*[@id="root"]/div[2]/div/div[1]/form/div[4]/div[2]/input')
    except Exception as e:
        print(f'ERROR LOG BUT \n{e}')

    while True:
        try:
            driver.implicitly_wait(10)
            find_error = driver.find_element(By.XPATH, '//div[@role="alert"]').text
            if "val" in find_error:
                input_data(driver, 50, '//*[@id="l_username"]', user_login)
                input_data(driver, 30, '//*[@id="l_password"]', user_password)

                print("Start solve captcha...")
                result = solver.recaptcha(site_key=site_key, page_url=url)
                print(f"РЕЗУЛЬТАТ: {str(result)}")

                driver.implicitly_wait(4.5)
                input_captcha_code = driver.find_element(By.TAG_NAME, 'textarea')
                driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result)

                try:
                    click(driver, 30, '//*[@id="root"]/div[2]/div/div[1]/form/div[4]/div[2]/input')
                except Exception as e:
                    print(f'ERROR LOG CLICK \n{e}')
            else:
                break
        except:
            break

    sleep(2.5)
    driver.get('https://www.seoclerk.com/order/2239')

    try:
        check_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="stripeButton"]'))
        )
        check_button.click()
    except Exception as e:
        driver.implicitly_wait(10)
        find_input_tag = driver.find_element(By.XPATH, '//*[@id="l_username"]')
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"CHECKOUT ERROR \n{e}")

    try:
        click(driver, 30, '//*[@id="nowPayments-form-btn"]')
    except Exception as e:
        print(f'ERROR CHOOSE NOWPAY')

    try:
        driver.implicitly_wait(60)
        click_select = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[1]/div[3]/div[1]')
        sleep(1.5)
        click_select.click()
    except Exception as e:
        print(f'ERROR SELECT \n{e}')

    try:
        click(driver, 30, '//img[@alt="Tether USD (Tron)"]')
        click(driver, 30, '//*[@id="payment-page"]/div/div[1]/div[1]/div[3]/button')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    while True:
        try:
            driver.implicitly_wait(7.5)
            find_error_text = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[1]/div[3]/div[3]')
            find_error_text.click()
        except:
            break


def get_wallet():
    try:
        with webdriver.Chrome(options=options) as driver:
            log = login(driver)
            if log:
                return log

            amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]'))
            )
            amount = amount.text.replace("USDT", "")

            address = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[1]'))
            )
            address = address.text

            return {
                "address": address,
                "amount": amount.replace("\n", '').replace("TRX", '').replace(' ', ''),
                "currency": "usdt"
            }
    except Exception as e:
        print(f"GET WALLET ERROR \n{e}")
        return None


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
