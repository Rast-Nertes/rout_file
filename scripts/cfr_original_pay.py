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

url = 'https://cfr-original.com/ru/'
user_email = "kiracase34@gmail.com"
user_password = "ud6_nPRefNzTa6"

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
        input_email = driver.find_element(By.XPATH, '/html/body/div[2]/aside/div[1]/form/label[1]/input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(15)
        input_password = driver.find_element(By.XPATH, '/html/body/div[2]/aside/div[1]/form/label[2]/input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '/html/body/div[2]/aside/div[1]/form/div[2]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")
    sleep(3)
    driver.get('https://cfr-original.com/ru/account/insert')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(30)
            input_amount = driver.find_element(By.XPATH, '//*[@id="payblock"]/label/input')
            input_amount.clear()
            input_amount.send_keys('550')

            driver.implicitly_wait(20)
            choose_pay = driver.find_element(By.XPATH, '//*[@id="accountinsert"]/div[2]/div[4]/div[2]/div/form[2]/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_pay)
        except Exception as e:
            print(f"ERROR CHOOSE \n{e}")

        try:
            sleep(5.5)
            driver.switch_to.window(driver.window_handles[1])
            driver.refresh()
            sleep(2)
        except Exception as e:
            print(f"SWITCH ERROR \n{e}")

        try:
            driver.implicitly_wait(50)
            choose_usdt = driver.find_element(By.XPATH, '(//div[@class="td"])[4]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_usdt)

            driver.implicitly_wait(50)
            input_email = driver.find_element(By.ID, 'id_order_email')
            input_email.clear()
            input_email.send_keys(user_email)

            driver.implicitly_wait(40)
            place_order = driver.find_element(By.XPATH, '/html/body/div/form/div[2]/div[4]/div[2]/a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", place_order)
        except Exception as e:
            print(f'ERROR CHOOSE USDT \n{e}')

        try:
            sleep(2.5)
            driver.implicitly_wait(90)
            address = driver.find_element(By.CSS_SELECTOR, 'div.amount__info.bb-info.attantion.blue-atantion > h3 > font:nth-child(6)').text

            driver.implicitly_wait(60)
            amount = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[1]/h3/font[1]').text.replace("USDT", '').replace(" ", '')

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
