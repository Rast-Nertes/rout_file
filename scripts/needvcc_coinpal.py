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
url = 'https://needvcc.com/product/buy-admaven-ads-accounts/'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

# proxy_address = "62.3.13.13"
# proxy_login = '1QjtPL'
# proxy_password = 'pHSyxy'
# proxy_port = 8000
#
# proxy_options = {
#     "proxy":{
#         "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
#         "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
#     }
# }

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(30)
        add_to_cart = driver.find_element(By.CSS_SELECTOR, 'div.summary.entry-summary > form > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", add_to_cart)
    except Exception as e:
        print(f'ERROR ADD TO CART \n{e}')

    sleep(3)
    driver.get('https://needvcc.com/checkout/')



def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(20)
            first_name = driver.find_element(By.ID, 'billing_first_name')
            first_name.clear()
            first_name.send_keys("Kira")

            driver.implicitly_wait(20)
            last_name = driver.find_element(By.ID, 'billing_last_name')
            last_name.clear()
            last_name.send_keys("Ivanova")

            driver.implicitly_wait(20)
            email = driver.find_element(By.ID, 'billing_email')
            email.clear()
            email.send_keys(user_email)
        except Exception as e:
            print(f'ERROR DATA INPUT \n{e}')

        try:
            sleep(5)
            driver.implicitly_wait(40)
            choose_coinpal = driver.find_element(By.ID, 'payment_method_coinpal')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_coinpal)
        except Exception as e:
            print(f'ERROR CHOOSE COINPAL \n{e}')

        try:
            sleep(1.5)
            driver.implicitly_wait(20)
            place_order = driver.find_element(By.ID, 'place_order')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", place_order)
        except Exception as e:
            print(f'ERROR PLACE ORDER \n{e}')

        try:
            driver.implicitly_wait(60)
            choose_usdt_trc20 = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_usdt_trc20)
        except Exception as e:
            print(f'ERROR CHOOSE USDT \n{e}')

        try:
            sleep(5)
            driver.implicitly_wait(50)
            address = driver.find_element(By.ID, 'qr_code').get_attribute('title')

            driver.implicitly_wait(10)
            amount = driver.find_element(By.CSS_SELECTOR, 'div > div.order_total > div:nth-child(1) > div.goods_total_value > span.total_span.total_span_blue').text.replace(" ", '')

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
