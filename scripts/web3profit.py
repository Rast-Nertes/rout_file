from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://web3profit.net/?a=login'
user_email = "alex37347818"
user_password = "JTYYyR2CVJHtxAZ"

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
        input_email = driver.find_element(By.CSS_SELECTOR, 'section > div > div > div > div > div > form > div:nth-child(6) > input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'section > div > div > div > div > div > form > div:nth-child(7) > input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'section > div > div > div > div > div > form > div.mb-3.mt-3 > input')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        sleep(2)
        driver.get('https://web3profit.net/?a=deposit')

        try:
            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.CSS_SELECTOR, '#processor > div > div > div:nth-child(11) > label')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(10)
            spend = driver.find_element(By.CSS_SELECTOR, 'div.member-content > div:nth-child(2) > div > form > div:nth-child(5) > div > div > div > div > div > div.middle-account > div > div > input.mt-3.btn.btn-primary')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", spend)
        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(40)
            address = driver.find_element(By.CSS_SELECTOR, '#coinpr_form > i > a').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, 'div.row.justify-content-center.mt-3 > div > div > div.card-body.p-5 > div > div.col-md-8 > table > tbody > tr:nth-child(8) > td').text

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


if __name__ == "__main__":
    wallet()