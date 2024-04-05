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

url = 'https://join.bigboobbundle.com/signup/signup.php?'
user_email = "yewoxo4550@otemdi.com"
user_password = "Qwerty62982"

# CHROME CONSTANS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    driver.execute_script("arguments[0].click();", elem_click)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


def login(driver):
    actions = ActionChains(driver)
    driver.get(url)
    driver.maximize_window()

    try:
        input_data(driver, 35, '//*[@id="username"]', 'rwork875')
        sleep(1)
        input_data(driver, 35, '//*[@id="password"]', user_password)
        sleep(1)
        input_data(driver, 20, '//*[@id="email"]', 'rwork875@gmail.com')
    except:
        print(f"ERROR INPUT DATA \n{e}")

    try:
        click(driver, 20, '//*[@id="Crypto"]/label')
    except Exception as e:
        print(f'ERROR CHOOSE CRYPTO \n{e}')

    try:
        click(driver, 20 , '//*[@id="join_form"]/div/div[2]/input')
    except Exception as e:
        print(f'ERROR SUBMIT \n{e}')

    try:
        click(driver, 35, '//*[@id="CryptoPurchaseButton"]')
    except Exception as e:
        print(f'ERROR NEXT STEP AFTER CHOOSE CRYPTO \n{e}')

    try:
        driver.implicitly_wait(30)
        select_crypto = driver.find_element(By.ID, 'CryptoPopupSelectWalletDdl')
        sleep(1.5)
        select_crypto.click()

        actions.send_keys(Keys.ARROW_DOWN).perform()
    except Exception as e:
        print(f'ERROR SELECT \n{e}')

    try:
        driver.implicitly_wait(10)
        select_trc20 = driver.find_element(By.ID, 'CryptoPopupSelectCurrencyDdl')
        sleep(1.5)
        select_trc20.click()

        for _ in range(19):
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.2)
        actions.send_keys(Keys.ENTER).perform()
        sleep(0.5)
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    sleep(3)

    try:
        driver.implicitly_wait(10)
        next_step_2 = driver.find_element(By.ID, 'CryptoPopupContinuePaymentButton')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", next_step_2)
    except Exception as e:
        print(f'ERROR NEXT STEP2 \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            sleep(5.5)
            driver.implicitly_wait(60)
            amount = driver.find_element(By.ID, 'CryptoPopupPaymentAmountValue').text

            driver.implicitly_wait(10)
            address = driver.find_element(By.ID, 'CryptoPopupOpenInWalletLink').get_attribute('data-alternative-url')

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
