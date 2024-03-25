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
url = 'https://www.bitcoingirlsflash.me/ru/auth/login'
user_email = "kiramira123"
user_password = "kiramira123123"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

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


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(20)
        accept = driver.find_element(By.XPATH, '//*[@id="react-app"]/div/div[2]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", accept)
    except:
        pass

    try:
        driver.implicitly_wait(40)
        input_email = driver.find_element(By.XPATH, '//*[@id="login"]/form/div[1]/input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '//*[@id="login"]/form/div[2]/input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'form > div.form-row.form-row--submit > button')
        sleep(3)
        driver.execute_script("arguments[0].click();", login_button)
        sleep(2)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        delete_element = driver.find_element(By.ID, 'form_token_login')
        sleep(1.5)
        driver.execute_script("arguments[0].parentNode.removeChild(arguments[0]);", delete_element)
    except Exception as e:
        print(f"ERROR DELETE ELEMENT \n{e}")

    sleep(15)

    try:
        driver.implicitly_wait(30)
        login_button = driver.find_element(By.CSS_SELECTOR, 'form > div.form-row.form-row--submit > button')
        sleep(3)
        driver.execute_script("arguments[0].click();", login_button)
        sleep(2)
    except Exception as e:
        print(f"ERROR CLICK BUTTON \n{e}")

    sleep(3)
    driver.get('https://www.bitcoingirlsflash.me/ru/free/payment')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(50)
            choose_payment = driver.find_element(By.XPATH, '//*[@id="overlay-container"]/section/div/div[2]/div[3]/p/span/a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_payment)
        except Exception as e:
            print(f"ERROR CHOOSE PAYMENT \n{e}")

        try:
            driver.implicitly_wait(50)
            choose_coingate = driver.find_element(By.XPATH, '//*[@id="firstbill-payment-method"]/div[2]/ul/li[8]/div/form/fieldset/input[5]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_coingate)
        except Exception as e:
            print(f'ERROR CHOOSE COINGATE \n{e}')

        try:
            driver.implicitly_wait(30)
            choose_method = driver.find_element(By.XPATH, '//*[@id="custom-packages"]/div/div[2]/div/div/div/form[1]/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_method)
        except Exception as e:
            print(f'ERROR CHOOSE METHOD \n{e}')

        try:
            driver.implicitly_wait(90)
            choose_usdt = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div/label[8]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_usdt)

            driver.implicitly_wait(20)
            continue_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button)
        except Exception as e:
            print(f"ERROR CHOOSE USDT \n{e}")

        try:
            driver.implicitly_wait(50)
            without_email = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[1]/div[2]/button[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", without_email)

            driver.implicitly_wait(50)
            choose_tron = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[3]/div/div/label[3]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_tron)

            driver.implicitly_wait(50)
            continue_button_2 = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div[2]/div/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button_2)
        except Exception as e:
            print(f"ERROR CHOOSE TRON \n{e}")

        driver.set_window_size(1200, 500)

        try:
            driver.implicitly_wait(60)
            amount = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/p').text.replace("USDT", '').replace(" ", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[6]/div/div[2]/div/p').text

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
