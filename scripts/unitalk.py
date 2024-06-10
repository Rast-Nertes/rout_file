from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from flask import Flask, jsonify
from twocaptcha import TwoCaptcha
from selenium import webdriver
from time import sleep

#thedex.cloud

#CONSTANS
user_login = 'kiracase34@gmail.com'
user_password = '0WvpZNBM'
url = 'https://my.unitalk.cloud/enter.html#auth'

#PROXY_CONSTANS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@45.130.254.133:8000",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}

#CHROME OPTIONS

options = webdriver.ChromeOptions()
options.add_argument("--disable-save-password-bubble")
options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.add_experimental_option("detach", True)


with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    ext = paths[1].strip()

options.add_extension(ext)


def js_click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    driver.execute_script("arguments[0].click();", elem_click)


def wait_visibility(driver, time, XPATH):
    WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.XPATH, XPATH))
    )
    sleep(2.5)


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
        js_click(driver, 30, '//*[@id="autoSolveHCaptcha"]')

        input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        js_click(driver, 30, '//*[@id="connect"]')
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
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/input')
        input_email.clear()
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/input')
        input_password.clear()
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        time_loop = 0
        while True:
            driver.implicitly_wait(10)
            find_check = driver.find_element(By.XPATH, '//div[@class="captcha-solver-info"]').text
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

    try:
        driver.implicitly_wait(10)
        button_login = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[6]/button')
        driver.execute_script("arguments[0].click();", button_login)
    except Exception as e:
        print(f"BUTTON ERROR \n{e}")
        return None

    sleep(5)


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        driver.get('https://my.unitalk.cloud/index.html#balance')

        try:
            driver.implicitly_wait(30)
            input_balance = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[1]/div[2]/div[2]/div/div/label/input')
            input_balance.send_keys('3')
        except Exception as e:
            print(f"INPUT BALANCE ERROR \n{e}")
            return None

        try:
            driver.implicitly_wait(10)
            add_value = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[1]/div[2]/div[2]/div/button')
            driver.execute_script("arguments[0].click();", add_value)
        except Exception as e:
            print(f"ADD VALUE BUTTON \n{e}")
            return None

        try:
            driver.implicitly_wait(10)
            choose_payment_method = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[3]/button')
            driver.execute_script("arguments[0].click();", choose_payment_method)

            driver.implicitly_wait(10)
            thedex_choose = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[3]/ul/li[2]')
            driver.execute_script("arguments[0].click();", thedex_choose)

            driver.implicitly_wait(10)
            buy_ = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/button')
            driver.execute_script("arguments[0].click();", buy_)
        except Exception as e:
            print(f"BUY BUTTON ERROR \n{e}")
            return None

        try:
            driver.implicitly_wait(10)
            tether_trc20 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div[1]/div/div[1]/div/div[2]/form/div[2]/ul/li[1]')
            driver.execute_script("arguments[0].click();", tether_trc20)

            driver.implicitly_wait(10)
            next_step = driver.find_element(By.XPATH, '//*[@id="btn-sub"]')
            driver.execute_script("arguments[0].click();", next_step)
        except Exception as e:
            print(f"TETHER TRC20 BUTTON ERROR \n{e}")
            return None
        
        
        driver.set_window_size(800, 400)
        sleep(2.5)
        amount = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[3]/div[1]/div[2]'))
        )
        amount = amount.text.replace(" ", "").replace("USDTTRC20", "")

        driver.implicitly_wait(40)
        address_elem = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[2]/div/div/a')
        address = address_elem.get_attribute('href').split('address')[1].replace("/", '')

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)


if __name__ == "__main__":
    wallet()