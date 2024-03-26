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
url = 'https://usaloqal.com/product/buy-aged-gmail-accounts/'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

proxy_address = "62.3.13.13"
proxy_login = '1QjtPL'
proxy_password = 'pHSyxy'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def login(driver):
    actions = ActionChains(driver)
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(40)
        choose_gmail = driver.find_element(By.ID, 'pa_aged_gmail_accounts')
        sleep(1.5)
        choose_gmail.click()

        actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()
        sleep(2.5)

        driver.implicitly_wait(20)
        submit_button = driver.find_element(By.XPATH, '//*[@id="product-297"]/div[2]/form/div/div[2]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", submit_button)
    except Exception as e:
        print(f"ERROR CHOOSE GMAIL \n{e}")

    sleep(3)
    driver.get('https://usaloqal.com/checkout/')


    sleep(5)
    try:
        driver.implicitly_wait(40)
        choose_coin = driver.find_element(By.ID, 'CsaltCoin')
        sleep(1.5)
        choose_coin.click()

        for _ in range(3):
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.5)

        actions.send_keys(Keys.ENTER).perform()
        sleep(0.5)
    except Exception as e:
        print(f"ERROR CHOOSE COIN \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(50)
            address = driver.find_element(By.ID, 'alt-coinAddress').get_attribute('value')

            driver.implicitly_wait(10)
            amount = driver.find_element(By.XPATH, '//*[@id="wapg_order_review"]/div/div/h3/strong').text

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
