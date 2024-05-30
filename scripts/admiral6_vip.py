from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://admiral6.vip'
user_email = "kiracase34@gmail.com"
user_password = "Mpqrd8njhFrdNx6"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
options.add_argument("--disable-save-password-bubble")
options.add_argument('--log-level=3')
options.add_argument('--disable-remote-fonts')
options.add_experimental_option('prefs', {'intl.accept_languages': 'en, en_US'})

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    ext = paths[1].strip()

# options.add_extension(ext)
# options.binary_location = chrome_path

# proxy_address = "45.142.119.179"
# proxy_login = '7GuQLH'
# proxy_password = 'GupxuD'
# proxy_port = 8000

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

# proxy_address = "196.19.121.187"
# proxy_login = 'WyS1nY'
# proxy_password = '8suHN9'
# proxy_port = 8000


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
        wait_visibility(driver, 60, '//*[@id="user-panel"]/div[1]/div/div[1]')
        click(driver, 30, '//*[@id="user-panel"]/div[1]/div/div[1]')
        input_data(driver, 30, '//*[@id="log_email"]', user_email)
        input_data(driver, 30, '//*[@id="log_pass"]', user_password)
        click(driver, 30, '//*[@id="log_button"]')
    except Exception as e:
        return {"status": "0", "ext": f"error login {e}"}

    try:
        click(driver, 10, '/html/body/div[1]/div/a[2]')
    except:
        pass

    try:
        wait_visibility(driver, 30, '//*[@id="kassa"]')
        click(driver, 30, '//*[@id="kassa"]')
        click(driver, 30, '//img[@data-depositway="crp"]')
        input_data(driver, 30, '//*[@id="depamount"]', '11')
        sleep(2.5)
        click(driver, 30, '//*[@id="submitdeposit"]')
    except Exception as e:
        return {"status":"0", "ext":f"error choose trc20 and input min amount \n{e}"}

    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        print(driver.title)
        sleep(1.5)
        if not("азин" in driver.title):
            break


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        try:
            wait_visibility(driver, 70, '//img[@alt="Tether"]')
            click(driver, 30, '//img[@alt="Tether"]')
            click(driver, 30, '//img[@alt="Tether TRC-20"]')
        except Exception as e:
            return {"status": "0", "ext": f"error choose trc20 {e}"}

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
            return {"status": "0", "ext": f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
