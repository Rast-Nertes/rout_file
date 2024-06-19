from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://pvashopusa.com/product/buy-old-gmail-accounts/'
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
        driver.implicitly_wait(45)
        choose_tov = driver.find_element(By.ID, 'pa_buy-gmail-accounts')
        choose_tov.click()
        sleep(1)
        actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()
    except Exception as e:
        print(f'ERROR CHOOSE \n{e}')

    try:
        click(driver, 20, '//*[@id="product-530"]/div[2]/form/div/div[2]/button')
    except Exception as e:
        print(f"ERROR ADD TO CART \n{e}")

    try:
        click(driver, 35, '//*[@id="post-9"]/div/div/div[2]/div/div/a')
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
        input_data(driver, 20, '//*[@id="billing_company"]', 'Company')
        sleep(0.5)
        input_data(driver, 20, '//*[@id="billing_address_1"]', 'Number 12')
        sleep(0.5)
        input_data(driver, 20, '//*[@id="billing_address_2"]', '12312')
        sleep(0.5)
        input_data(driver, 20, '//*[@id="billing_city"]', 'City')
    except Exception as e:
        print(f'ERROR INPUT DATA 1 \n{e}')

    try:
        input_data(driver, 20, '//*[@id="billing_postcode"]', '11223')
        sleep(0.5)
        input_data(driver, 20, '//*[@id="billing_phone"]', '+79800801122')
    except Exception as e:
        print(f'ERROR INPUT DATA 2 \n{e}')

    try:
        driver.implicitly_wait(30)
        choose_tron = driver.find_element(By.ID, 'mcc_currency_id')
        select = Select(choose_tron)

        select.select_by_value("USDT_TRON")
    except Exception as e:
        print(f'ERROR CHOOSE TRON \n{e}')

    try:
        sleep(2.5)
        click(driver, 20, '//*[@id="place_order"]')
    except Exception as e:
        print(f'ERROR INPUT TERMS \n{e}')

    try:
        click(driver, 20, '//*[@id="place_order"]')
    except Exception as e:
        print(f"ERROR PLACE ORDER \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(35)
            amount = driver.find_element(By.XPATH, '//*[@id="post-642"]/div/div/div/div/div/div/div/div/div[2]/div/p/span[1]/span/input').get_attribute('value').replace("USDT_TRON", '').replace(" ", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="post-642"]/div/div/div/div/div/div/div/div/div[2]/div/p/span[2]/span/input').get_attribute('value')

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
