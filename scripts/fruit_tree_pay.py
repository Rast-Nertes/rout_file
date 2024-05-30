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

url = 'https://s1.fruit-tree.lol/login'
user_email = "kiracase34@gmail.com"
user_password = "E9nvJLtnYzSr296"

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
        input_data(driver, 35, '/html/body/div/div/div[2]/form/input[1]', user_email)
        sleep(1)
        input_data(driver, 20, '/html/body/div/div/div[2]/form/input[2]', user_password)
        sleep(1)
        click(driver, 20 ,'/html/body/div/div/div[2]/form/span/input')
    except Exception as e:
        return {"status":"0", "ext":f"error input data {e}"}

    try:
        click(driver, 20, '/html/body/div[3]/div[2]/div/div[2]/a')
    except Exception as e:
        return {"status":"0", "ext":f"error next step {e}"}

    try:
        driver.implicitly_wait(20)
        click_pay = driver.find_element(By.XPATH, '/html/body/div[3]/div[3]/div[2]/b/div/div[1]')
        sleep(2.5)
        click_pay.click()
    except Exception as e:
        return {"status":"0", "ext":f"error choose pay {e}"}

    try:
        input_data(driver, 30, '//*[@id="psevdo"]', '650')
        sleep(1)
        click(driver, 20, '//*[@id="submit"]')
    except Exception as e:
        return {"status":"0", "ext":f"error input amount {e}"}

    try:
        click(driver, 20, '/html/body/div[3]/div[3]/b/center/form/input[7]')
    except Exception as e:
        return {"status":"0", "ext":f"error next {e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(50)
            choose_usdt = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[3]/ul[1]/li[4]')
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
            return {"status":"0", "ext":f"error choose usdt {e}"}

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
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
