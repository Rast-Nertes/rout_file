from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS
#form_token_login
url = 'https://roposh.com/product/zambia-passport-template-in-psd-format-fully-editable/'
user_email = "kiracase34"
user_password = "MnQ-wM6-Njf-i2y"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(30)
        add_to_cart_button = driver.find_element(By.XPATH, '//*[@id="product-35444"]/div[2]/form/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", add_to_cart_button)
    except Exception as e:
        print(f'ERROR ADD TO CART \n{e}')

    try:
        driver.implicitly_wait(30)
        view_cart_button = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/div/a')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", view_cart_button)

        driver.implicitly_wait(40)
        checkout_button = driver.find_element(By.XPATH, '//*[@id="post-2871"]/div/div/div[2]/div/div/a')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", checkout_button)
    except Exception as e:
        print(f'ERROR VIEW CART \n{e}')

    try:
        driver.implicitly_wait(30)
        click_log = driver.find_element(By.XPATH, '//*[@id="post-2872"]/div/div/div[2]/div/a')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", click_log)
    except Exception as e:
        print(f"ERROR CLICK LOG \n{e}")

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.ID, 'username')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.ID, 'password')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/main/article/div/div/form[1]/p[4]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    try:
        driver.implicitly_wait(30)
        place_order = driver.find_element(By.ID, 'place_order')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", place_order)
    except Exception as e:
        print(f'ERROR PLACE ORDER \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(50)
            select_currency = driver.find_element(By.XPATH,
                                                  '//*[@id="payment-page"]/div/div[1]/div[1]/div[3]/div[1]/div')
            sleep(1.5)
            select_currency.click()

            driver.implicitly_wait(30)
            choose_tron = driver.find_element(By.XPATH,
                                              '//*[@id="payment-page"]/div/div[1]/div[1]/div[3]/div[1]/div[2]/div[2]/ul/li[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_tron)

            driver.implicitly_wait(30)
            next_step = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[1]/div[3]/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step)
        except Exception as e:
            print(f"ERROR CHOOSE TRON \n{e}")

        try:
            sleep(5.5)
            driver.implicitly_wait(70)
            address = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[1]').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]').text.replace("USDT", '').replace("TRX", '').replace(" ", '').replace("\n", '')

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
