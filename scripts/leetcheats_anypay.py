from flask import jsonify
from selenium_driverless.sync import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

url = 'https://leet-cheats.ru/signin'
user_email = "kiracase34"
user_password = "wyD37QVnCRweg8h"

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.binary_location = chrome_path


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        input_email = driver.find_element(By.CSS_SELECTOR, 'div.container > div > div > div:nth-child(1) > div > form > div.input-group.mb-3 > input', timeout=30)
        input_email.clear()
        input_email.write(user_email)

        input_password = driver.find_element(By.CSS_SELECTOR, 'div.container > div > div > div:nth-child(1) > div > form > div.input-group.mb-4 > input', timeout=20)
        input_password.clear()
        input_password.write(user_password)

        login_button = driver.find_element(By.CSS_SELECTOR, 'div.container > div > div > div:nth-child(1) > div > form > button', timeout=10)
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    sleep(2)
    driver.get('https://leet-cheats.ru/profile')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            append_amount = driver.find_element(By.CSS_SELECTOR, 'div > div.col-12.col-md > div > div.row.mt-3.mt-md-0 > div:nth-child(1) > button:nth-child(3)', timeout=20)
            sleep(1.5)
            driver.execute_script("arguments[0].click();", append_amount)
        except Exception as e:
            print(f"APPEND AMOUNT \n{e}")

        try:
            input_amount = driver.find_element(By.ID, 'fillup_balance__amount', timeout=20)
            sleep(2)
            input_amount.write("100")
        except Exception as e:
            print(f"INPUT ERROR \n{e}")

        try:
            next_step = driver.find_element(By.XPATH, '//*[@id="balanceEditor"]/div/div/form/div[2]/button[1]', timeout=30)
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step)
        except Exception as e:
            print(f"ERROR CHOOSE PAYMENT \n{e}")

        try:
            find_frame = driver.find_elements(By.TAG_NAME, 'iframe')
            sleep(1)
            iframe_document = find_frame[0].content_document

            checkbox = iframe_document.find_element(By.CSS_SELECTOR,
                                                          '#challenge-stage > div > label > span.ctp-label', timeout=20)
            sleep(3)
            checkbox.click()
        except Exception as e:
            print(f"CLICK \n{e}")

        try:
            choose_tether = driver.find_element(By.XPATH, '/html/body/main/div[2]/div[1]/div[2]/div[2]/div[8]', timeout=30)
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_tether)

            button_buy = driver.find_element(By.CSS_SELECTOR, 'div.form > form > div.group.button > button', timeout=30)
            sleep(1.5)
            driver.execute_script("arguments[0].click();", button_buy)
        except Exception as e:
            print(f"TETHER CHOOSE ERROR \n{e}")

        try:
            address = driver.find_element(By.CSS_SELECTOR, 'div > form > div.group.address.float > fieldset > input[type=text]', timeout=30).__getattribute__('value')

            amount = driver.find_element(By.CSS_SELECTOR, 'div > form > div.group.details > div.amount > span', timeout=30).text.replace("USDT", '').replace(" ", '')

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
