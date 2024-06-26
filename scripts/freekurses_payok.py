from flask import jsonify
from selenium import webdriver
from time import sleep
import urllib.parse
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CONSTANS

user_login = 'kiracase34@gmail.com'
user_password = '9eeHhLkJuWTTAKK'
url = 'https://freekurses.site/moj-akkaunt/'

#API CONSTANS

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.ID, 'username')
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.ID, 'password')
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"INPUT DATA ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '//*[@id="customer_login"]/div[1]/form/p[3]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN BUTTON ERROR \n{e}")


def get_wallet(driver):
    login(driver)
    driver.get('https://freekurses.site/product/natalja-minina-osobennosti-sevooborota-na-ovoshhah-2024/')
    try:
        driver.implicitly_wait(20)
        button_in_busket = driver.find_element(By.XPATH, '//*[@id="product-523205"]/div[2]/form/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", button_in_busket)
    except Exception as e:
        print(f"ADD TO BUSKET ERROR \n{e}")

    driver.get('https://freekurses.site/wishlist/cart/')

    try:
        driver.implicitly_wait(20)
        input_count = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/main/article/div/div/form/table/tbody/tr[1]/td[5]/div/input')
        sleep(2)
        input_count.clear()
        input_count.send_keys('10')
    except Exception as e:
        print(f"INPUT COUNT ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        refresh_busket = driver.find_element(By.XPATH, '//*[@id="post-57"]/div/div/form/table/tbody/tr[2]/td/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", refresh_busket)
    except Exception as e:
        print(f"REFRESH BUSKET \n{e}")

    sleep(1.5)
    driver.get('https://freekurses.site/wishlist/checkout/')


def choose_payment_method():
    with webdriver.Chrome(options=options) as driver:
        get_wallet(driver)

        #input("1")

        try:
            driver.implicitly_wait(10)
            choose_payeer = driver.find_element(By.CSS_SELECTOR, 'ul > li.wc_payment_method.payment_method_payok > label')
            driver.execute_script("arguments[0].click();", choose_payeer)
        except Exception as e:
            print(f"CHOOSE PAYEER ERROR \n{e}")

        sleep(3)
        try:
            driver.implicitly_wait(20)
            accept_choose = driver.find_element(By.CSS_SELECTOR, '#place_order')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", accept_choose)
        except Exception as e:
            print(f"PLACE ORDER ERROR \n{e}")

        try:
            driver.implicitly_wait(30)
            choose_trc20 = driver.find_element(By.CSS_SELECTOR, '#pay_tether_trc_button_open')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(10)
            input_email_ = driver.find_element(By.CSS_SELECTOR, '#pay_tether_trc_generate_form > fieldset.pay_input_crypto_block > input[type=email]')
            sleep(1.5)
            input_email_.clear()
            input_email_.send_keys(user_login)
        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            sunbmit_button = driver.find_element(By.ID, 'pay_tether_trc_generate_button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", sunbmit_button)
        except Exception as e:
            print(f"SUBMIT BUTTON ERROR \n{e}")

        try:
            sleep(5)
            src_element = driver.find_element(By.XPATH, '/html/body/main/div[1]/div[3]/div[7]/div[2]/div[4]/div/div[2]/img')
            src = src_element.get_attribute('src')

            parsed_url = urllib.parse.urlparse(src)
            query_params = urllib.parse.parse_qs(parsed_url.query)

            address = query_params['chl'][0].split(':')[1].split('?')[0]
            amount = query_params['chl'][0].split('=')[1]

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = choose_payment_method()
    print(wallet_data)
    return jsonify(wallet_data)
