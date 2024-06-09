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

url = 'https://buyusabank.com/product/buy-scarlet-bank-account/'
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
        driver.implicitly_wait(40)
        add_to_cart = driver.find_element(By.XPATH, '//*[@id="product-432"]/div[2]/form/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", add_to_cart)

        sleep(3)
        driver.get('https://buyusabank.com/checkout/')
    except Exception as e:
        print(f'ERROR ADD TO CART \n{e}')

    try:
        driver.implicitly_wait(20)
        input_firts_name = driver.find_element(By.ID, 'billing_first_name')
        input_firts_name.clear()
        input_firts_name.send_keys("Kira")

        driver.implicitly_wait(20)
        input_last_name = driver.find_element(By.ID, 'billing_last_name')
        input_last_name.clear()
        input_last_name.send_keys("Ivanova")

        driver.implicitly_wait(20)
        input_email = driver.find_element(By.ID, 'billing_email')
        input_email.clear()
        input_email.send_keys(user_email)
    except Exception as e:
        return {"status": "0", "ext": f"error input data {e}"}

    try:
        sleep(4.5)
        driver.implicitly_wait(10)
        choose_coinpal = driver.find_element(By.ID, 'payment_method_coinpal')
        sleep(1.5)
        driver.execute_script('arguments[0].click();', choose_coinpal)
    except Exception as e:
        print(f"ERROR CHOOSE COINPAL \n{e}")

    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="place_order"]'))
        )
        sleep(2.5)
        place_order = driver.find_element(By.XPATH, '//*[@id="place_order"]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", place_order)
    except Exception as e:
        return {"status":"0", "ext":f"error place order {e}"}

    try:
        driver.implicitly_wait(40)
        choose_trc20 = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div/div/div[2]/div[1]/div[1]/div[2]/div[2]')
        sleep(1.5)
        driver.execute_script('arguments[0].click();', choose_trc20)
    except Exception as e:
        print(f"ERROR CHOOSE TRC20 \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div/div/div[2]/div[1]/div[5]/div[1]/div/div[1]/div[4]/span').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div/div/div[2]/div[1]/div[5]/div[1]/div/div[1]/div[2]/span').text.replace("USDT ($20.00)", "").replace(" ", "")

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
