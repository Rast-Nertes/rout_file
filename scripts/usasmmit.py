from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://usasmmit.com'
user_login = "kiracase34@gmail.com"
user_password = "kiramira555"

#PROXY_CONSTANS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@45.130.254.133:8000",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        actions = ActionChains(driver)
        driver.get(url)
        driver.maximize_window()

        try:
            driver.implicitly_wait(10)
            purchase_button = driver.find_element(By.CSS_SELECTOR, '#prctbl9 > a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", purchase_button)
        except Exception as e:
            print(f"PURCHASE BUTTON ERROR \n{e}")

        try:
            # driver.implicitly_wait(10)
            # input_count = driver.find_element(By.CSS_SELECTOR, '#quantity_65e02fff83238')
            # sleep(1.5)
            # input_count.clear()
            # input_count.send_keys("1")
            #
            # driver.implicitly_wait(10)
            # update_cart = driver.find_element(By.CSS_SELECTOR, 'div.rh-container.clearfix.mt30.mb30 > div > article > div > form > table > tbody > tr:nth-child(2) > td > button')
            # sleep(1.5)
            # driver.execute_script("arguments[0].click();", update_cart)

            driver.implicitly_wait(10)
            proceed_to_checkout = driver.find_element(By.CSS_SELECTOR, 'div.rh-container.clearfix.mt30.mb30 > div > article > div > div.cart-collaterals > div > div > a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", proceed_to_checkout)
        except Exception as e:
            print(f"INPUT ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_first_name = driver.find_element(By.ID, 'billing_first_name')
            input_first_name.clear()
            input_first_name.send_keys("Kira")

            driver.implicitly_wait(10)
            input_last_name = driver.find_element(By.ID, 'billing_last_name')
            input_last_name.clear()
            input_last_name.send_keys("Ivanova")

            driver.implicitly_wait(10)
            input_email_address = driver.find_element(By.ID, 'billing_email')
            input_email_address.clear()
            input_email_address.send_keys(user_login)
        except Exception as e:
            print(f"INPUT DATA ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            ticket = driver.find_element(By.ID, 'terms')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", ticket)
            sleep(5)
        except Exception as e:
            print(f"TICKET ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            choose_currency = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/article/div/form[2]/div[2]/div/div/ul/li[1]/div/fieldset/p/select')
            sleep(2)
            choose_currency.click()

            for _ in range(3):
                actions.send_keys(Keys.ARROW_DOWN).perform()
                sleep(0.5)

            actions.send_keys(Keys.ENTER).perform()
            sleep(5)
        except Exception as e:
            print(f"CHOOSE CURRENCY ERROR \n{e}")

        try:
            driver.implicitly_wait(30)
            address = driver.find_element(By.ID, 'alt-coinAddress').get_attribute("value")

            driver.implicitly_wait(30)
            amount = driver.find_element(By.CSS_SELECTOR, '#wapg_order_review > table > tbody > tr > td.product-name > strong').text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }

        except Exception as e:
            print(f"DATA ERROR \n{e}")
            return None


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
