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

url = 'https://account.richmedia.today/login'
user_email = "alex37347818@gmail.com"
user_password = "mufUsxDW1M7"

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
        input_email = driver.find_element(By.CSS_SELECTOR, '#kt_sign_in_form > div.fv-row.mb-8.fv-plugins-icon-container > input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, '#kt_sign_in_form > div.fv-row.mb-3.fv-plugins-icon-container > input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.ID, 'kt_sign_in_submit')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)

        sleep(6.5)
        driver.get('https://account.richmedia.today/replenishment')

    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(10)
            next_step = driver.find_element(By.CSS_SELECTOR, '#kt_modal_top_up_wallet_stepper_form > div.d-flex.flex-stack.pt-1 > div:nth-child(2) > button:nth-child(2)')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step)

            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.XPATH, '//*[@id="kt_modal_top_up_wallet_stepper_form"]/div[2]/div/div[4]/div/div/div[4]/label')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(10)
            submit_button = driver.find_element(By.XPATH, '//*[@id="kt_modal_top_up_wallet_stepper_form"]/div[4]/div[2]/button[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit_button)
        except Exception as e:
            print(f"TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_amount_trc20 = driver.find_element(By.CSS_SELECTOR, '#kt_modal_top_up_wallet_stepper_form > div.current > div.w-100.crypto-topup > div.mb-10.fv-row > input')
            input_amount_trc20.clear()
            input_amount_trc20.send_keys("5")

            driver.implicitly_wait(10)
            next_step_button = driver.find_element(By.CSS_SELECTOR, '#kt_modal_top_up_wallet_stepper_form > div.d-flex.flex-stack.pt-1 > div:nth-child(2) > button.btn.btn-lg.btn-primary.d-inline-block')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step_button)
        except Exception as e:
            print(f"ERROR INPUT \n{e}")

        try:
            driver.implicitly_wait(40)
            address = driver.find_element(By.ID, 'kt_referral_link_input').get_attribute('value')

            driver.implicitly_wait(20)
            amount = driver.find_element(By.CSS_SELECTOR, '#kt_modal_top_up_wallet_stepper_form > div.current > div.w-100.crypto-topup > div > p:nth-child(2) > strong > input').get_attribute('value').replace('USDT.TRC20', '').replace(" ", '')

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