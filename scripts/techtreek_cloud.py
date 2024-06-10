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

url = 'https://bd.techtreek.com/store/south-carolina-driver-license-psd-template/'
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
        add_to_cart = driver.find_element(By.XPATH, '//*[@id="product-2670"]/div[2]/form/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", add_to_cart)

        driver.implicitly_wait(50)
        proceed_button = driver.find_element(By.XPATH, '//*[@id="post-39"]/div/div/section[2]/div/div/div/div/div/div/div[2]/div[2]/div/div/a')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", proceed_button)
    except Exception as e:
        print(f"ERROR ADD TO CART \n{e}")

    try:
        driver.implicitly_wait(20)
        skip_login = driver.find_element(By.ID, 'wpmc-skip-login')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", skip_login)
    except Exception as e:
        print(f"ERROR SKIP LOGIN BUTTON \n{e}")

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
        input_city = driver.find_element(By.ID, 'billing_city')
        input_city.clear()
        input_city.send_keys("City")
    except Exception as e:
        print(f"ERROR 1 PART DATA \n{e}")

    try:
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
        place_order = driver.find_element(By.ID, 'wpmc-next')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", place_order)
    except Exception as e:
        print(f"ERROR PLACE ORDER \n{e}")

    try:
        driver.implicitly_wait(30)
        place_order = driver.find_element(By.ID, 'wpmc-next')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", place_order)
    except Exception as e:
        print(f"ERROR PLACE ORDER \n{e}")

    try:
        driver.implicitly_wait(30)
        choose_cloud = driver.find_element(By.ID, 'payment_method_cryptocloud')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", choose_cloud)

        sleep(3.5)
        driver.implicitly_wait(50)
        terms = driver.find_element(By.ID, 'terms')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", terms)
    except Exception as e:
        print(f"ERROR CHOOSE \n{e}")

    try:
        driver.implicitly_wait(30)
        place_order_but = driver.find_element(By.ID, 'place_order')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", place_order_but)
    except Exception as e:
        print(f"ERROR PLACE ORDER \n{e}")

    try:
        click_next = WebDriverWait(driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[3]/button'))
        )
        driver.execute_script("arguments[0].click();", click_next)
    except Exception as e:
        print(f"ERROR CLICK NEXT \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(7.5)
            driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div/input')
        except Exception as e:
            click_next = WebDriverWait(driver, 40).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[3]/button'))
            )
            driver.execute_script("arguments[0].click();", click_next)

        try:
            driver.implicitly_wait(50)
            address = driver.find_element(By.XPATH,
                                          '//*[@id="app"]/div/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div/span').text
            sleep(1.5)

            driver.implicitly_wait(10)
            amount = driver.find_element(By.XPATH,
                                         '//*[@id="app"]/div/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/span').text.replace(
                "USDT", '').replace(" ", '')

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
