from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://trex.casino/'
user_email = "kiracase34@gmail.com"
user_password = "nP5Dei4isBbJz6@"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
options.add_argument("--disable-save-password-bubble")
options.add_argument('--log-level=3')
options.add_argument('--disable-remote-fonts')
options.add_experimental_option('prefs', {'intl.accept_languages': 'en, en_US'})

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


def wait_visibility(driver, time, XPATH):
    WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.XPATH, XPATH))
    )
    sleep(2.5)


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    elem_click.click()


def js_click(driver, time, XPATH):
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
    driver.maximize_window()
    driver.get(url)

    try:
        wait_visibility(driver, 40, '/html/body/header/nav/div[2]/a[2]')
        click(driver, 10, '/html/body/header/nav/div[2]/a[2]')
    except Exception as e:
        return {"status":"0", "ext":f"error path to login {e}"}

    try:
        wait_visibility(driver, 30, '//*[@id="username"]')
        input_data(driver, 10, '//*[@id="username"]', user_email)
        input_data(driver, 10, '//*[@id="password"]', user_password)
        click(driver, 30, '//*[@id="signin"]/div/div/form/div[2]/input')
    except Exception as e:
        return {"status":"0", "ext":f"error login {e}"}

    try:
        wait_visibility(driver, 30, '(//input[@class="btn btn-success"])[1]')
        sleep(2)
        js_click(driver, 10, '(//input[@class="btn btn-success"])[1]')
    except Exception as e:
        return {"status":"0", "ext":f"error sign in button {e}"}

    try:
        wait_visibility(driver, 30, '//div[@class="cash"]')
        click(driver, 10, '//div[@class="cash"]')
    except Exception as e:
        return {"status":"0", "ext":f"error click depos but {e}"}

    try:
        wait_visibility(driver, 30, '(//select)[1]')
        select_elem = driver.find_element(By.XPATH, '(//select)[1]')
        select = Select(select_elem)
        select.select_by_value('Crypto')
        click(driver, 10, '//input[@class="btn btn-success _btn-deposit cashin_but"]')
    except Exception as e:
        return {"status":"0", "ext":f"error choose crypto {e}"}

    try:
        wait_visibility(driver, 30, '(//img[@alt="Tether USDT"])[1]')
        js_click(driver, 10, '(//img[@alt="Tether USDT"])[1]')
        sleep(1.5)
        click(driver, 10, '//button[@type="button"]')
    except Exception as e:
        return {"status":"0", "ext":f"error choose trc20 {e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//*[@id="app"]/main/section/div/div/div[2]/div[2]/ul/li[2]/div[1]')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="app"]/main/section/div/div/div[2]/div[2]/ul/li[1]/div[1]')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace("TRC20", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)