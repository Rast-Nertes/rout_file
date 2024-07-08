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

url = 'https://corgislot.com/'
user_email = "rwork875@gmail.com"
user_password = "0993644El"

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
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


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
    driver.get(url)
    driver.maximize_window()

    try:
        click(driver, 20, '//*[@id="root"]/div/main/aside/div[2]/div/button[2]')
    except Exception as e:
        print(f'ERROR LOG BUT \n{e}')

    try:
        input_data(driver, 30, '//*[@id="email"]', user_email)
        sleep(1)
        input_data(driver, 20, '//*[@id="password"]', user_password)
        sleep(1)
        click(driver, 20, '//*[@id="root"]/div/div[2]/div/div[2]/div/div[1]/div[2]/button')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        click(driver, 20, '//*[@id="14"]')
        sleep(1)

        click(driver, 20, '//*[@id="depositPromocode"]/div[4]/div/div/p')
        sleep(1)
        click(driver, 20, '//*[@id="depositPromocode"]/div[4]/div/div[2]/div[7]')
    except Exception as e:
        print(f'ERROR Choose net\n{e}')

    try:
        click(driver, 20, '//*[@id="depositPromocode"]/div[3]/button[1]')
    except Exception as e:
        print(f'ERROR input min amount \n{e}')

    try:
        click(driver, 20, '//*[@id="depositPromocode"]/div[9]/button')
    except Exception as e:
        print(f"ERROR DEPOS BUT \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/div/p[4]/span').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div[2]/div/div/p[2]/span').text.replace("USDTTRC20", '').replace(" ", '')

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