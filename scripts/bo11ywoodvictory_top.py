from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://bo11ywoodvictory.top/#authorization'
user_email = "kiracase34@gmail.com"
user_password = "KAiW6ev3wiDhfFy"

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
        input_data(driver, 60, '//input[@type="email"]', user_email)
        input_data(driver, 30, '//input[@type="password"]', user_password)
        js_click(driver, 30,'//*[@id="__layout"]/div/div[3]/div/section/section/section[1]/section/div[2]/button/span[3]')
    except Exception as e:
        return {"status":"0", "ext":f"error login {e}"}

    sleep(5)
    driver.get('https://bo11ywoodvictory.top/payment/deposit?step=2&nameComponent=RequisitesFillOut&paymentSystemId=177')

    try:
        WebDriverWait(driver, 40).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/main/div/div/div/section/div/section/section/section[2]/div[2]/form/fieldset/div[1]/div[2]/div/input'))
        )
        sleep(5)
        input_data(driver, 30, '//*[@id="__layout"]/div/main/div/div/div/section/div/section/section/section[2]/div[2]/form/fieldset/div[1]/div[2]/div/input', user_email)
        js_click(driver, 30,'//*[@id="__layout"]/div/main/div/div/div/section/div/section/section/section[2]/div[2]/form/fieldset/div[3]/div[1]/label')
        js_click(driver, 30,'//*[@id="__layout"]/div/main/div/div/div/section/div/section/section/section[2]/div[2]/form/div/button/span[3]')
    except Exception as e:
        return {"status":"0", "ext":f"error input amount {e}"}

    sleep(10)
    handles = driver.window_handles
    print(handles)
    for handle in handles:
        driver.switch_to.window(handle)
        title = driver.title
        if not ("каз" in title):
            break

    try:
        sleep(5)
        input_data(driver, 80, '//*[@id="react-select-2-input"]', 'trc20')
        sleep(1.5)
        actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()
        sleep(1)
        js_click(driver, 39,'//*[@id="root"]/div/div/div[2]/div/div/div[2]/form/div[5]/div/div/div/div/label/span[1]/input')
    except Exception as e:
        return {"status":"0", "ext":f"error choose trc20 {e}"}

    try:
        js_click(driver, 30, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/form/div[6]/div/div/div/button')
    except Exception as e:
        return {"status":"0", "ext":f"error submit button {e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            address_elem = driver.find_element(By.XPATH, '//input[@name="address"]')
            address = address_elem.get_attribute('value')

            print(address)

            amount_elem = driver.find_element(By.CSS_SELECTOR, 'div > div > h2')
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
