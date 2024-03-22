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

url = 'https://verifstore.com/item/kupit-akkaunt-paxful-s-verifikaciej-nedorogo'
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
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.XPATH, '//*[@id="itemlinksdesk257"]/div[4]/div[1]/div[4]/input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(30)
        input_email = driver.find_element(By.XPATH, '//*[@id="itemlinksdesk257"]/div[4]/div[1]/div[2]/input')
        input_email.clear()
        input_email.send_keys("1")

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div[1]/div/div/div/div[4]/div[1]/div[5]/button[2]')
        sleep(4)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(10)
            next_step_button = driver.find_element(By.XPATH, '//*[@id="paymodal"]/div/div/div[3]/a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step_button)
        except Exception as e:
            print(f"ERROR NEXT STEP \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.ID, 'currency-15')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"INPUT EMAIL \n{e}")

        try:
            driver.implicitly_wait(10)
            submit_payment = driver.find_element(By.ID, 'submit-payment')
            sleep(1.5)
            submit_payment.click()
        except Exception as e:
            print(f"SUBMIT ERROR \n{e}")

        try:
            driver.implicitly_wait(40)
            address = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[7]/div[2]').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[5]/span').text

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