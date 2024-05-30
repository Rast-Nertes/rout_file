from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://games-of-thrones.com/login'
user_email = "kiracase34@gmail.com"
user_password = "RBbH$tG$am49AZY"
site_key = '6LfB0fAoAAAAAGh_HziuH-kUo3Qay30h-9IiNrde'

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
        js_click(driver, 30, '//*[@id="autoSolveHCaptcha"]')

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


def login(driver):
    api_connect(driver)
    driver.get(url)
    driver.maximize_window()

    try:
        input_data(driver, 20, '//input[@type="text"]', user_email)
        input_data(driver, 20, '//input[@type="password"]', user_password)

        try:
            time_loop = 0
            while True:
                driver.implicitly_wait(10)
                find_check = driver.find_element(By.XPATH, '(//div[@class="captcha-solver-info"])').text
                if ("ена" in find_check) or ("lve" in find_check):
                    break
                else:
                    if time_loop > 120:
                        return {"status": "0", "ext": "CAPTCHA ERROR"}
                    time_loop += 5
                    sleep(5)
                    print("Wait 5 seconds, captcha solving...")
        except Exception as e:
            print(f'ERROR CHECKBOX')

        driver.implicitly_wait(10)
        log_but = driver.find_element(By.XPATH, '//*[@id="login"]/div/div[6]/center/div/div/button/div[2]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", log_but)
    except Exception as e:
        return {"status":"0", "ext":f"error login {e}"}

    try:
        click(driver, 20, '//*[@id="btu-prompt-login_required"]/div/div[2]/div/div[1]/div/button/div[1]')
    except:
        pass

    try:
        click(driver,20, '/html/body/div[7]/div[4]/div[1]/div/div[17]')
    except Exception as e:
        return {"status":"0", "ext":f"error add balance {e}"}

    try:
        click(driver, 20, '//button[@class="psusdt"]')
    except Exception as e:
        return {"status":"0", "ext":f"error choose crypto payment {e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '//*[@id="main_deposit_address"]').get_attribute('value')

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
