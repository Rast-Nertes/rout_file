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

url = 'https://macros.fun/'
user_email = "kiracase34@gmail.com"
user_password = "nP5Dei4isBbJz6@"

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

# proxy_address = "45.130.254.133"
# proxy_login = 'K0nENe'
# proxy_password = 'uw7RQ3'
# proxy_port = 8000

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
        wait_visibility(driver, 40, '/html/body/div[6]/div[2]/div[2]/a[2]')
        href = driver.find_element(By.XPATH, '/html/body/div[6]/div[2]/div[2]/a[2]').get_attribute('href')
        driver.get(href)
    except Exception as e:
        return {"status":"0", "ext":f"error get href {e}"}

    try:
        wait_visibility(driver, 30, '//*[@id="fPay"]/div/label/label')
        js_click(driver, 10, '//*[@id="fPay"]/div/label/label')
        js_click(driver, 10, '//*[@id="btn_next"]')
    except Exception as e:
        return {"status":"0", "ext":f"error proceed button error {e}"}

    try:
        wait_visibility(driver, 50, '//*[@id="TypeCurr_msdd"]')
        js_click(driver, 10, '//*[@id="TypeCurr_msdd"]')
        js_click(driver, 10, "//span[@class='ddlabel' and text()='USDT']")
    except Exception as e:
        return {"status":"0", "ext":f"error choose usdt {e}"}

    try:
        wait_visibility(driver, 20, '//*[@id="email"]')
        input_data(driver, 10, '//*[@id="email"]', user_email)
        input_data(driver, 10, '//*[@id="Re_Enter_Email"]', user_email)
        js_click(driver, 10, '//*[@id="pay_btn"]')
    except Exception as e:
        return {"status":"0", "ext":f"error depos {e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//*[@id="form1"]/section/section/div[2]/div[2]/div[4]/div/div[1]/div/span')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="form1"]/section/section/div[2]/div[2]/div[4]/p/span')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
