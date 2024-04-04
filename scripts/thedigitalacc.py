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

url = 'https://thedigitalacc.com/p/aws-account-for-sale/'
user_email = "gifebeb534@sfpixel.com"
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
        choose_tov = driver.find_element(By.XPATH, '//*[@id="options"]')
        choose_tov.click()
        sleep(1)
        actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()
    except Exception as e:
        print(f'ERROR CHOOSE \n{e}')

    try:
        click(driver, 20, '//*[@id="product-336"]/div[2]/div[2]/form/div/div[2]/button')
    except Exception as e:
        print(f"ERROR ADD TO CART \n{e}")

    try:
        click(driver, 35, '//*[@id="content"]/div/div/div/div[2]/div/section/div/div/div/div/div/div/div[2]/div/div/a')
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
        click(driver, 20, '//*[@id="payment_method_wc_payerurl_gateway"]')
        sleep(3.5)
        click(driver, 20, '//*[@id="terms"]')
    except Exception as e:
        print(f'ERROR INPUT TERMS \n{e}')

    try:
        click(driver, 20, '//*[@id="place_order"]')
    except Exception as e:
        print(f"ERROR PLACE ORDER \n{e}")

    try:
        click(driver, 35, '/html/body/div[2]/div[2]/div/div[2]/div/a[2]')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(35)
            address = driver.find_element(By.ID, 'add_val').get_attribute('value')

            driver.implicitly_wait(10)
            amount = driver.find_element(By.ID, 'amt_val').text

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