from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from anticaptchaofficial.imagecaptcha import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://nanogames.io/login'
user_email = "kiracase34@gmail.com "
user_password = "tVXi@yhT3arPEPG"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
options.add_argument("--disable-save-password-bubble")
options.add_argument('--log-level=3')
options.add_argument('--disable-remote-fonts')
options.add_experimental_option('prefs', {'intl.accept_languages': 'en, en_US'})

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[2].strip()
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


def solve_captcha():
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(api_key)
    captcha_text = solver.solve_and_return_solution("captcha.jpeg")
    return captcha_text


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
        sleep(4.5)
        input_data(driver, 60, '/html/body/div[7]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/input', user_email)
        input_data(driver, 30, '/html/body/div[7]/div/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/input', user_password)
        click(driver, 30, '//*[@id="login"]/div[2]/button[1]')
        sleep(2)
    except Exception as e:
        return {"status":"0", "ext":f"error login {e}"}

    while True:
        try:
            driver.implicitly_wait(5)
            driver.find_element(By.XPATH, '//img[@class="verify-img"]').screenshot('captcha.jpeg')

            result = solve_captcha()

            driver.implicitly_wait(10)
            input_captcha = driver.find_element(By.XPATH, '(//div[@class="input-control"]/input)[3]')
            input_captcha.send_keys(result)

            click(driver, 30, '//*[@id="login"]/div[2]/button[1]')
            sleep(5)
        except Exception as e:
            print(f'ERROR CAPTCHA ')
            break

    sleep(3.5)
    driver.get('https://nanogames.io/wallet/deposit')

    try:
        driver.implicitly_wait(10)
        close = driver.find_element(By.XPATH, '//button[@class="close flex-center"]')
        close.click()
    except :pass

    try:
        click(driver, 30, '//*[@id="deposit"]/div[3]/div[1]/div[2]/div/div[3]/button')
    except Exception as e:
        print(f'ERROR CLICK TRC20 \n{e}')
        input("pr")
        return {"status": "0", "ext": f"error trc20 {e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//input[@class="address"]')
            address = address_elem.get_attribute('value')

            return {
                "address": address,
                "amount": "0.01",
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
