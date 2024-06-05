from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#PAYMENTARS

#CONSTANS

user_login = 'kiracase34@gmail.com'
user_password = '9eeHhLkJuWTTAKK'
url = 'https://freekurses.site/moj-akkaunt/'

#API CONSTANS
api_key = '7f728c25edca4f4d0e14512d756d6868'

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False


def wait_visibility(driver, time, XPATH):
    WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.XPATH, XPATH))
    )
    sleep(2.5)


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.ID, 'username')
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.ID, 'password')
        input_password.send_keys(user_password)
    except Exception as e:
        return {"status":"0", "ext":f"error input data {e}"}

    try:
        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '//*[@id="customer_login"]/div[1]/form/p[3]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        return {"status":"0", "ext":f"error log button  {e}"}


def get_wallet(driver):
    login(driver)
    driver.get('https://freekurses.site/product/natalja-minina-osobennosti-sevooborota-na-ovoshhah-2024/')
    try:
        driver.implicitly_wait(20)
        button_in_busket = driver.find_element(By.XPATH, '//*[@id="product-523205"]/div[2]/form/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", button_in_busket)
    except Exception as e:
        return {"status":"0", "ext":f"error add to busket {e}"}

    driver.get('https://freekurses.site/wishlist/cart/')

    try:
        driver.implicitly_wait(20)
        input_count = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/main/article/div/div/form/table/tbody/tr[1]/td[5]/div/input')
        sleep(2)
        input_count.clear()
        input_count.send_keys('1')
    except Exception as e:
        return {"status":"0", "ext":f"error count input {e}"}

    try:
        driver.implicitly_wait(10)
        refresh_busket = driver.find_element(By.XPATH, '//*[@id="post-57"]/div/div/form/table/tbody/tr[2]/td/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", refresh_busket)
    except Exception as e:
        return {"status":"0", "ext":f"error refresh busket  {e}"}

    sleep(1.5)
    driver.get('https://freekurses.site/wishlist/checkout/')


def choose_payment_method():
    with webdriver.Chrome(options=options) as driver:
        get_wallet(driver)

        try:
            sleep(6.5)
            wait_visibility(driver, 30, '//label[@for="payment_method_cryptocloud"]')
            choose_crypto_cloud_payment = driver.find_element(By.XPATH, '//label[@for="payment_method_cryptocloud"]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_crypto_cloud_payment)
        except Exception as e:
            return {"status":"0", "ext":f"error choose crypto {e}"}

        try:
            sleep(1.5)
            wait_visibility(driver, 15, '(//input[@type="email"])[1]')
            input_email = driver.find_element(By.XPATH, '(//input[@type="email"])[1]')
            input_email.send_keys(user_login)

            driver.implicitly_wait(10)
            accept_choose = driver.find_element(By.ID, 'place_order')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", accept_choose)
        except Exception as e:
            return {"status":"0", "ext":f"error accept choose {e}"}

        try:
            wait_visibility(driver, 30, '(//button[@target="_blank"])[2]')
            buy_with_trc_20 = driver.find_element(By.XPATH, '(//button[@target="_blank"])[2]')
            sleep(1.5)
            buy_with_trc_20.click()
        except:
            try:
                driver.refresh()
                driver.implicitly_wait(50)
                buy_with_trc_20 = driver.find_element(By.XPATH, '(//button[@target="_blank"])[2]')
                sleep(1.5)
                buy_with_trc_20.click()
            except Exception as e:
                return {"status":"0", "ext":f"error click buy button {e}"}

        try:
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div/span'))
            )

            driver.implicitly_wait(30)
            address = driver.find_element(By.XPATH,
                                          '//*[@id="app"]/div/div/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div/span').text
            driver.implicitly_wait(30)
            amount = driver.find_element(By.XPATH,
                                         '//*[@id="app"]/div/div/div/div[2]/div[2]/div[2]/div[3]/div[1]/span[2]').text.replace("USDT", '')
            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = choose_payment_method()
    print(wallet_data)
    return jsonify(wallet_data)
