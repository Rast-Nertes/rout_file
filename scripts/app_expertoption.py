from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://app.expertoption.com'
user_email = "kejokan542@haislot.com"
user_password = "Qwerty17"

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

# options.binary_location = chrome_path
options.add_extension(ext)

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


def js_click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    driver.execute_script("arguments[0].click();", elem_click)


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


def api_connect(driver):
    sleep(1.5)
    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        sleep(1.5)
        if "2Cap" in driver.title:
            break

    try:
        js_click(driver, 30, '//*[@id="autoSolveRecaptchaV2"]')
        js_click(driver, 30, '//*[@id="autoSolveInvisibleRecaptchaV2"]')
        js_click(driver, 30, '//*[@id="autoSolveRecaptchaV3"]')
        input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        click(driver, 30, '//*[@id="connect"]')
        sleep(4.5)
        driver.switch_to.alert.accept()
    except Exception as e:
        print(f'ERROR CLICK \n{e}')

    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        sleep(1.5)
        if not("2Cap" in driver.title):
            break


def login(driver):
    api_connect(driver)
    driver.maximize_window()
    driver.get("https://app.expertoption.com/login")

    try:
        click(driver, 90, '//div[@data-testid="at_login_tab"]')
        input_data(driver, 90, '//*[@id="app"]/div/div/div/div/div/div[1]/div[5]/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[1]/div[1]/div/input', user_email)
        input_data(driver, 60, '//*[@id="app"]/div/div/div/div/div/div[1]/div[5]/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div/div/div[2]/div[1]/div[3]/div/input', user_password)
        click(driver, 30, '//div[@data-testid="at_login_button"]')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')
        return {"status": "0", "ext": f"Login error \n{e}"}

    try:
        driver.implicitly_wait(90)
        get_href = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div/div[1]/div[5]/div[2]/div[1]/div/div/div/div[1]/div[2]/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/iframe').get_attribute('src')
        driver.get(get_href)
    except Exception as e:
        return {"status": "0", "ext": f"GET SRC \n{e}"}

    try:
        click(driver, 90, '//*[@id="root"]/div/div/div[1]/div/div[2]/div/button[6]')
        click(driver, 60, '//*[@id="root"]/div/div/div[1]/div[1]/div[8]/button')
        click(driver, 30, '//*[@id="root"]/div/div/div[1]/div[6]/div/div/button')
        click(driver, 30, '//*[@id="root"]/div/div/div[1]/div/div[2]/div/button')
    except Exception as e:
        return {"status": "0", "ext": f"CHOOSE CRYPTO \n{e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(7.5)
        try:
            driver.implicitly_wait(60)
            address_elem = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/section[2]/div[2]/div/div/input')
            address = address_elem.get_attribute('value')

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[1]/div/section[1]/div[1]/span/span')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("$", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
