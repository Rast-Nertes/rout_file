from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS
#form_token_login
url = 'https://buyaccounts.io/product/buy-canva-premium-account/'
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
        buy_button = driver.find_element(By.CSS_SELECTOR, 'div.summary.entry-summary > form > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", buy_button)
    except Exception as e:
        print(f"ERROR BUY BUTTON \n{e}")

    try:
        driver.implicitly_wait(20)
        input_email = driver.find_element(By.ID, 'username')
        input_email.clear()
        input_email.send_keys('kiracase34@gmail.com')

        driver.implicitly_wait(20)
        input_pass = driver.find_element(By.ID, 'password')
        input_pass.clear()
        input_pass.send_keys('GMGvPVNgm3Jen5E')

        driver.implicitly_wait(20)
        log_button = driver.find_element(By.XPATH, '//*[@id="checkout_login"]/form/p[4]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", log_button)
    except Exception as e:
        print(f"ERROR LOG BUTTON \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(30)
            input_first_name = driver.find_element(By.ID, 'billing_first_name')
            input_first_name.clear()
            input_first_name.send_keys("Kira")

            driver.implicitly_wait(30)
            input_second_name = driver.find_element(By.ID, 'billing_last_name')
            input_second_name.clear()
            input_second_name.send_keys("Ivanova")

            driver.implicitly_wait(30)
            telegram_id = driver.find_element(By.ID, 'billing_telegram')
            telegram_id.clear()
            telegram_id.send_keys('112233')

            driver.implicitly_wait(30)
            next_button = driver.find_element(By.ID, 'wpmc-next')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_button)
        except Exception as e:
            print(f"ERROR NEXT BUTTON \n{e}")

        try:
            driver.implicitly_wait(30)
            choose_usdt = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/section[2]/div/div/div/div/div/div/div[5]/form/div[2]/div[2]/ul/b/li/label')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_usdt)
        except Exception as e:
            print(f"ERROR INPUT DATA \n{e}")

        try:
            sleep(3.5)
            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="payment"]/ul/b/li/div/fieldset/b').text

            driver.implicitly_wait(10)
            amount = driver.find_element(By.XPATH, '//*[@id="order_review"]/table/tfoot/tr[2]/td/strong/span/bdi').text.replace("$", '')

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
