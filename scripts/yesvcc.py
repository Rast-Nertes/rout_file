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

url = 'https://yesvcc.com/product/buy-aws-vcc-account/'
user_email = "yewoxo4550@otemdi.com"
user_password = "Qwerty62982"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1)
    driver.execute_script("arguments[0].click();", elem_click)
    sleep(1)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


def login(driver):
    actions = ActionChains(driver)
    driver.get(url)
    driver.maximize_window()

    try:
        click(driver, 40, '//button[@name="add-to-cart"]')
    except Exception as e:
        print(f"ERROR ADD TO CART \n{e}")

    try:
        click(driver, 35, '//*[@id="post-8"]/div/div/div[2]/div/div/a')
    except Exception as e:
        print(f'ERROR PROCEED \n{e}')

    try:
        input_data(driver, 35, '//*[@id="billing_first_name"]', "Kira")
        sleep(0.5)
        input_data(driver, 20 , '//*[@id="billing_last_name"]', "Ivanova")
        sleep(0.5)
        input_data(driver, 20, '//*[@id="billing_email"]', user_email)
    except Exception as e:
        print(f"ERROR INPUT DATA \n{e}")

    try:
        click(driver, 20, '//*[@id="payment_method_coinpal"]')
        sleep(3.5)
        click(driver, 20, '//*[@id="place_order"]')
    except Exception as e:
        print(f'ERROR INPUT TERMS \n{e}')

    try:
        click(driver, 35, '//*[@id="__layout"]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div[2]')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(35)
            amount = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div/div/div[2]/div[1]/div[5]/div[1]/div/div[1]/div[2]/span').text.replace("USDT", '').split('(')[0].strip().replace(" ", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div/div/div[2]/div[1]/div[5]/div[1]/div/div[1]/div[4]/span').text

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
