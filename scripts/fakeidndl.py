from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://fakeidndl.com/product/buy-connecticut-fake-ids/'
user_email = "kiracase34@gmail.com"
user_password = "Kiramira000"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    ext = paths[1].strip()

options.binary_location = chrome_path
# options.add_extension(ext)

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
    actions = ActionChains(driver)

    try:
        click(driver, 30, '//*[@id="product-1461"]/div[1]/div[2]/form/button')

        click(driver, 30, '//*[@id="post-7"]/div/div/div[2]/div/div/a')
    except Exception as e:
        print(f'ERROR LINK \n{e}')

    try:
        input_data(driver, 30, '//*[@id="billing_first_name"]', "Kira")
        input_data(driver, 30, '//*[@id="billing_last_name"]', "Ivanova")
        input_data(driver, 30, '//*[@id="billing_address_1"]', "11223")
        input_data(driver, 30, '//*[@id="billing_city"]', 'City')
        input_data(driver, 30, '//*[@id="billing_postcode"]', "11223")
        input_data(driver, 30, '//*[@id="billing_phone"]', "+11223344555")
        input_data(driver, 30, '//*[@id="billing_email"]', user_email)
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    try:
        click(driver, 30, '//*[@id="place_order"]')
    except Exception as e:
        print(f'ERROR CLICK ORDER BUT \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        try:
            click(driver, 30, '//img[@alt="Tether"]')
            click(driver, 30, '//img[@alt="Tether TRC-20"]')
        except Exception as e:
            print(f'ERROR CHOOSE TETHER \n{e}')

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.CLASS_NAME, 'step-pay__address')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="step_pay__amount_payTo"]')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("\n", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)