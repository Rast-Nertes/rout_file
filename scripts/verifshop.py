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
url = 'https://verifshop.com/item/binance-account-verification-Intermediate'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(50)
        input_email = driver.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div:nth-child(4) > input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div:nth-child(2) > input')
        input_password.clear()
        input_password.send_keys('1')

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.ID, 'bbb')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    try:
        driver.implicitly_wait(30)
        sleep(5)
        go_toPayment = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[1]/div[2]/div/div/div[3]/a')
        sleep(1.5)
        driver.get(go_toPayment.get_attribute('href'))
    except Exception as e:
        print(f"ERROR GO TO PAYMENT \n{e}")

    driver.refresh()
    sleep(3)
    try:
        click_next = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[3]/button'))
        )
        driver.execute_script("arguments[0].click();", click_next)
    except Exception as e:
        print(f"ERROR CLICK NEXT \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(7.5)
            driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div/input')
        except Exception as e:
            click_next = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[3]/button'))
            )
            driver.execute_script("arguments[0].click();", click_next)

        try:
            driver.implicitly_wait(50)
            address = driver.find_element(By.XPATH,
                                          '/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div/span').text
            sleep(1.5)

            driver.implicitly_wait(10)
            amount = driver.find_element(By.XPATH,
                                         '/html/body/div[1]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/span').text.replace(
                "USDT", '').replace(" ", '')

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
