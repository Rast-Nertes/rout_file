from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://bankdoc.net/product/buy-australia-bank-statement/'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def login(driver):
    actions = ActionChains(driver)
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(30)
        input_first_name = driver.find_element(By.ID, 'input_13_15')
        input_first_name.clear()
        input_first_name.send_keys("Kira")

        driver.implicitly_wait(30)
        input_address_1 = driver.find_element(By.ID, 'input_13_11_1')
        input_address_1.clear()
        input_address_1.send_keys("1 Street")

        driver.implicitly_wait(30)
        input_city = driver.find_element(By.ID, 'input_13_11_3')
        input_city.clear()
        input_city.send_keys("City")
    except Exception as e:
        return {"status":"0", "ext":f"error first part data {e}"}

    try:
        driver.implicitly_wait(30)
        input_zipcode = driver.find_element(By.ID, 'input_13_11_5')
        input_zipcode.clear()
        input_zipcode.send_keys("12345")

        driver.implicitly_wait(30)
        input_email_0 = driver.find_element(By.ID, 'input_13_16_2')
        input_email_0.clear()
        input_email_0.send_keys(user_email)

        driver.implicitly_wait(30)
        input_email = driver.find_element(By.ID, 'input_13_16')
        input_email.clear()
        input_email.send_keys(user_email)
    except Exception as e:
        return {"status":"0", "ext":f"error second part data {e}"}

    sleep(2.5)

    try:
        driver.implicitly_wait(30)
        place_order = driver.find_element(By.ID, 'gform_submit_button_13')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", place_order)
    except Exception as e:
        return {"status":"0", "ext":f"error place order {e}"}

    sleep(3.5)

    try:
        driver.implicitly_wait(30)
        view_cart = driver.find_element(By.XPATH, '//*[@id="main-content"]/div[2]/div/div[4]/div/div/span/a[1]')
        sleep(1.5)
        driver.execute_script('arguments[0].click();', view_cart)
    except Exception as e:
        return {"status":"0", "ext":f"error view {e}"}

    try:
        driver.implicitly_wait(50)
        checkout_button = driver.find_element(By.XPATH, '//*[@id="post-33941"]/div[1]/div[2]/div/div[2]/div/div[2]/div/a')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", checkout_button)
    except Exception as e:
        return {"status":"0", "ext":f"error checkout {e}"}

    try:
        driver.implicitly_wait(30)
        input_first_name = driver.find_element(By.ID, 'billing_first_name')
        input_first_name.clear()
        input_first_name.send_keys("Kira")

        driver.implicitly_wait(30)
        input_last_name = driver.find_element(By.ID, 'billing_last_name')
        input_last_name.clear()
        input_last_name.send_keys("Ivanova")

        driver.implicitly_wait(30)
        input_address_1 = driver.find_element(By.ID, 'billing_address_1')
        input_address_1.clear()
        input_address_1.send_keys("1 Street")

        driver.implicitly_wait(30)
        input_city = driver.find_element(By.ID, 'billing_city')
        input_city.clear()
        input_city.send_keys("City")
    except Exception as e:
        return {"status": "0", "ext": f"error first part data, step 2  {e}"}

    try:
        driver.implicitly_wait(30)
        input_zipcode = driver.find_element(By.ID, 'billing_postcode')
        input_zipcode.clear()
        input_zipcode.send_keys("12345")

        driver.implicitly_wait(30)
        input_email = driver.find_element(By.ID, 'billing_email')
        input_email.clear()
        input_email.send_keys(user_email)
    except Exception as e:
        return {"status":"0", "ext":f"error second part data step 2 {e}"}

    sleep(5)

    try:
        driver.implicitly_wait(50)
        choose_select = driver.find_element(By.XPATH, '//*[@id="mcc_currency_id_field"]/span')
        sleep(1.5)
        driver.execute_script("arguments[0].setAttribute('style', 'cursor: pointer;')", choose_select)
        sleep(1.5)

        choose_select.click()
        for _ in range(8):
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.2)
        actions.send_keys(Keys.ENTER).perform()
        sleep(0.5)
    except Exception as e:
        return {"status":"0", "ext":f"error choose trc20  {e}"}

    try:
        driver.implicitly_wait(30)
        place_order_2 = driver.find_element(By.ID, 'place_order')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", place_order_2)
    except Exception as e:
        return {"status":"0", "ext":f"error place order {e}"}


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        sleep(3.5)
        try:
            driver.implicitly_wait(50)
            amount = driver.find_element(By.XPATH, '//*[@id="post-33942"]/div[1]/div[2]/div/div/div[2]/div/p/span[1]/span/input').get_attribute('value').replace("USDT_TRON", '').replace(" ", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="post-33942"]/div[1]/div[2]/div/div/div[2]/div/p/span[2]/span/input').get_attribute('value')

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
