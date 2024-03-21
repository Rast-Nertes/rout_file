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

url = 'https://coinstash.online/i/'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def login(driver):
    actions = ActionChains(driver)
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        send_select = driver.find_element(By.ID, 'give')
        sleep(1.5)
        send_select.click()

        actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(0.5)
        actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()
    except Exception as e:
        print(f"ERROR CHOOSE TRC20 \n{e}")

    try:
        driver.implicitly_wait(10)
        take_select = driver.find_element(By.ID, 'take')
        sleep(1.5)
        take_select.click()

        actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(0.5)
        actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()
    except Exception as e:
        print(f"ERROR TAKE \n{e}")

    try:
        driver.implicitly_wait(10)
        wash_button = driver.find_element(By.ID, 'cleanupButton')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", wash_button)
    except Exception as e:
        print(f"WASH BUTTON ERROR \n{e}")

    try:
        driver.implicitly_wait(30)
        input_amount = driver.find_element(By.ID, 'send-amount')
        input_amount.clear()
        input_amount.send_keys('251')

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div.block-content.block-content-full > form > div.row > div:nth-child(2) > div.row > div.col-12.col-md-7 > div > input')
        input_password.clear()
        input_password.send_keys("11111")

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '//*[@id="main-container"]/div[1]/div[1]/div[2]/form/div[3]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="merchant-detail"]').get_attribute('value')

            driver.implicitly_wait(10)
            amount = driver.find_element(By.XPATH, '//*[@id="merchant-amount"]').get_attribute('value')

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
