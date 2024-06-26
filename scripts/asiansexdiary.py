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
url = 'https://asiansexdiary.com/'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}

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
        choose_crypto = driver.find_element(By.CSS_SELECTOR, '#menu-main-menu-1 > a > li')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", choose_crypto)
    except Exception as e:
        print(f"ERROR CHOOSE CRYPTO \n{e}")

    try:
        driver.implicitly_wait(80)
        input_email = driver.find_element(By.ID, 'my_customer_email')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.ID, 'my_agreementFirstStep')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '//*[@id="stepButtons"]/div[2]/div[3]/button/span')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(60)
            choose_trc20 = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div[3]/div[2]/div/div[10]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"ERROR CHOOSE TRC20 \n{e}")

        sleep(7.5)
        try:
            driver.implicitly_wait(30)
            address = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div[1]').text

            driver.implicitly_wait(10)
            amount = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[2]/div[3]').text

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
