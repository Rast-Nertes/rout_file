import pyautogui
import pyperclip
from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://metaspins.com/#sign-in'
user_email = "kiracase34@gmail.com"
user_password = "Pxs6*FW9s.M2jy!"

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

options.add_extension(ext)
# options.binary_location = chrome_path

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000
#
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
    api_connect(driver)
    driver.get(url)

    try:
        input_data(driver, 30, '//input[@data-testid="input-email-login"]', user_email)
        sleep(0.5)
        input_data(driver, 30, '//input[@data-testid="input-password-login"]', user_password)
        sleep(0.5)
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    try:
        time_loop = 0
        while True:
            driver.implicitly_wait(15)
            find_check = driver.find_element(By.XPATH, '//*[@id="signin-recaptcha"]/div/div[2]/div[2]').text
            if ("ена" in find_check) or ("lve" in find_check):
                sleep(2.5)
                click(driver, 30, '//button[@data-testid="final-login-button"]')
                print("Complete")
                break
            else:
                if time_loop > 120:
                    return {"status": "0", "ext": "CAPTCHA ERROR"}
                time_loop += 5
                sleep(5)
                print("Wait 5 seconds, captcha solving...")
    except Exception as e:
        print(f'ERROR CHECKBOX \n{e}')

    sleep(6.5)
    driver.get('https://metaspins.com/casino#deposit')

    try:
        click(driver, 30, '//*[@id="modal"]/div/div/div/div[2]/div[1]/div[2]/div/div[1]')
        click(driver, 30, '//*[@id="modal"]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/p')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(1.5)
        try:
            click(driver, 30, '//button[@data-testid="currency-address"]')
            sleep(2.5)
            address = pyperclip.paste()
            # input("press")

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div/div/div[2]/div[2]/p[1]')
            amount = amount_elem.text.replace("USDT", '').replace("(5 USD)", '').replace("", '').replace(" ", '')

            return {
                "address": address,
                "amount": amount[-1],
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
