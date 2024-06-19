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
url = 'https://smmseomarket.com/product/buy-old-gmail-account/'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

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


def login(driver):
    actions = ActionChains(driver)
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(30)
        select_method = driver.find_element(By.ID, 'pa_buy-old-gmail-account')
        sleep(1.5)
        select_method.click()

        actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()
    except Exception as e:
        print(f"ERROR SELECT \n{e}")

    try:
        driver.implicitly_wait(30)
        add_to_cart_button = driver.find_element(By.CSS_SELECTOR, 'form > div > div.woocommerce-variation-add-to-cart.variations_button.woocommerce-variation-add-to-cart-enabled > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", add_to_cart_button)

        driver.implicitly_wait(50)
        view_cart = driver.find_element(By.CSS_SELECTOR, 'div.woocommerce-notices-wrapper > div > a')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", view_cart)
    except Exception as e:
        print(f"ERROR ADD TO CART BUTTON \n{e}")

    try:
        driver.implicitly_wait(50)
        proceed_to_checkout = driver.find_element(By.XPATH, '//*[@id="post-422"]/div/div/div[2]/div/div/a')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", proceed_to_checkout)
    except Exception as e:
        print(f"ERROR PROCEED BUTTON \n{e}")

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
        input_company = driver.find_element(By.ID, 'billing_company')
        input_company.clear()
        input_company.send_keys("Company")

        driver.implicitly_wait(30)
        input_address_1 = driver.find_element(By.ID, 'billing_address_1')
        input_address_1.clear()
        input_address_1.send_keys("1 Street")

        driver.implicitly_wait(30)
        input_address_2 = driver.find_element(By.ID, 'billing_address_2')
        input_address_2.clear()
        input_address_2.send_keys("112233")

        driver.implicitly_wait(30)
        input_city = driver.find_element(By.ID, 'billing_city')
        input_city.clear()
        input_city.send_keys("City")
    except Exception as e:
        print(f"ERROR 1 PART DATA \n{e}")

    try:
        driver.implicitly_wait(30)
        input_zipcode = driver.find_element(By.ID, 'billing_postcode')
        input_zipcode.clear()
        input_zipcode.send_keys("12345")

        driver.implicitly_wait(30)
        input_phone = driver.find_element(By.ID, 'billing_phone')
        input_phone.clear()
        input_phone.send_keys("+79800807781")

        driver.implicitly_wait(30)
        input_email = driver.find_element(By.ID, 'billing_email')
        input_email.clear()
        input_email.send_keys(user_email)
    except Exception as e:
        print(f"ERROR 2 PART DATA \n{e}")

    sleep(4)

    try:
        driver.implicitly_wait(30)
        place_order = driver.find_element(By.ID, 'place_order')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", place_order)
    except Exception as e:
        print(f"ERROR PLACE ORDER \n{e}")

    try:
        sleep(5)
        driver.implicitly_wait(40)
        choose_trc20 = driver.find_element(By.XPATH, '(//button[@type="button"])[2]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", choose_trc20)
    except Exception as e:
        print(f"ERROR CHOOSE TRC20 \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '(//input)[2]').get_attribute('value')

            driver.implicitly_wait(10)
            amount = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/div[2]/div/div/p[1]/span[1]').text

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
