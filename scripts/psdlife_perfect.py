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

url = 'https://psdlife.com/product/albania-id-card-psd-template-physical-appearance-of-the-biometric-id/'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"
perfect_id = '84286029'
perfect_pass = 'kdUqfuz1'

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
# options.add_argument('--headless')

#PROXY_CONSTANS

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@196.19.121.187:8000",
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


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        actions = ActionChains(driver)
        driver.get(url)
        driver.maximize_window()

        try:
            driver.implicitly_wait(70)
            add_to_cart_button = driver.find_element(By.CSS_SELECTOR, 'div > div.summary.entry-summary.col-md-7 > form > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", add_to_cart_button)

            sleep(2)
            driver.get('https://psdlife.com/checkout/')

            driver.implicitly_wait(30)
            proceed_to_check = driver.find_element(By.CSS_SELECTOR, '#panel-cart-total > div > div > a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", proceed_to_check)
        except Exception as e:
            print(f"ERROR ADD CART \n{e}")

        try:
            driver.implicitly_wait(20)
            input_first_name = driver.find_element(By.ID, 'billing_first_name')
            input_first_name.clear()
            input_first_name.send_keys("Kira")

            driver.implicitly_wait(20)
            input_last_name = driver.find_element(By.ID, 'billing_last_name')
            input_last_name.clear()
            input_last_name.send_keys('Ivanova')

            driver.implicitly_wait(20)
            input_email = driver.find_element(By.ID, 'billing_email')
            input_email.send_keys(user_email)
        except Exception as e:
            print(f"DATA ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_perfect = driver.find_element(By.XPATH, '//*[@id="payment"]/ul/li[2]/div[1]/label')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_perfect)
            sleep(5)
        except Exception as e:
            print(f"ERROR CHOOSE PERFECT \n{e}")

        try:
            driver.implicitly_wait(30)
            place_order = driver.find_element(By.ID, 'place_order')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", place_order)
        except Exception as e:
            print(f"ERROR PERFECT \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_crypto = driver.find_element(By.ID, 'r_crypto')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_crypto)

            driver.implicitly_wait(10)
            make_payment_start = driver.find_element(By.CSS_SELECTOR, 'td > table:nth-child(4) > tbody > tr > td > table > tbody > tr > td > div > form > table:nth-child(5) > tbody > tr > td:nth-child(1) > input')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", make_payment_start)
        except Exception as e:
            print(f'ERROR MAKE PAYMENT \n{e}')

        try:
            driver.implicitly_wait(10)
            input_member_id = driver.find_element(By.CSS_SELECTOR, 'tr > td > table > tbody > tr:nth-child(1) > td:nth-child(2) > input[type=text]')
            sleep(1.5)
            input_member_id.send_keys(perfect_id)

            driver.implicitly_wait(10)
            input_name = driver.find_element(By.ID, 'keyboardInputInitiator0')
            input_name.clear()
            input_name.send_keys(perfect_pass)
        except Exception as e:
            print(f"ERROR CHOOSE CRYPTO CURRENCY \n{e}")

        driver.set_window_size(400, 400)
        driver.execute_script("document.body.style.zoom='350%'")
        driver.execute_script("window.scrollBy(185, 1750);")
        sleep(3)
        driver.save_screenshot('captcha.jpg')
        sleep(1)
        driver.maximize_window()
        driver.execute_script("document.body.style.zoom='100%'")

        result = captcha_solver()
        sleep(3)
        try:
            driver.implicitly_wait(10)
            input_result_captcha = driver.find_element(By.XPATH, '/html/body/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[3]/td[1]/div[1]/form/table[1]/tbody/tr/td/table/tbody/tr[3]/td[2]/input')
            sleep(1.5)
            input_result_captcha.send_keys(result)
        except Exception as e:
            print(f"ERROR INPUT RESULT \n{e}")

        try:
            driver.implicitly_wait(10)
            make_payment = driver.find_element(By.XPATH, '//*[@id="f_log"]/table[2]/tbody/tr[2]/td[1]/input')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", make_payment)
        except Exception as e:
            print(f'MAKE PAYMENT ERROR \n{e}')

        try:
            driver.implicitly_wait(60)
            choose_trc20 = driver.find_element(By.XPATH, '//*[@id="auth"]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table[2]/tbody/tr/td/table/tbody/tr/td/div/form/table[1]/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/td[2]/label[2]/table')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(20)
            make_payment_2 = driver.find_element(By.CSS_SELECTOR, 'table:nth-child(4) > tbody > tr > td > table > tbody > tr > td > div > form > table:nth-child(2) > tbody > tr:nth-child(2) > td:nth-child(1) > input')
            driver.execute_script("arguments[0].click();", make_payment_2)
        except Exception as e:
            print(f"ERROR CHOOSE TRC20 \n{e}")

        try:
            driver.implicitly_wait(30)
            amount = driver.find_element(By.CSS_SELECTOR, 'tbody > tr > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(3) > td:nth-child(2)').text.replace('USDT', '').replace(' ', '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR, 'table:nth-child(4) > tbody > tr > td > table > tbody > tr > td > div > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(4) > td:nth-child(2)').text

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
