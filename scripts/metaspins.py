import pyautogui
from flask import jsonify
from seleniumwire import webdriver
from time import sleep
import pyperclip
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://metaspins.com/'
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

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def api_connect(driver):
    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        print(driver.title)
        sleep(1.5)
        if "2Cap" in driver.title:
            break

    try:
        input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        click(driver, 30, '//*[@id="connect"]')
        sleep(5.5)
        driver.switch_to.alert.accept()
        click(driver, 30, '//*[@id="autoSolveRecaptchaV2"]')
        click(driver, 30, '//*[@id="autoSolveInvisibleRecaptchaV2"]')
        click(driver, 30, '//*[@id="autoSolveRecaptchaV3"]')
    except Exception as e:
        print(f'ERROR CLICK \n{e}')

    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        print(driver.title)
        sleep(1.5)
        if not("2Cap" in driver.title):
            break


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
    driver.maximize_window()
    api_connect(driver)
    driver.get(url)
    # actions = ActionChains(driver)

    try:
        click(driver, 30, '//button[@data-testid="login-button"]')
    except Exception as e:
        print(f'ERROR CLICK LOGIN BUT \n{e}')

    try:
        input_data(driver, 30, '//input[@data-testid="input-email-login"]', user_email)
        input_data(driver, 30, '//input[@data-testid="input-password-login"]', user_password)

        time_loop = 0
        while True:
            driver.implicitly_wait(10)
            find_check = driver.find_element(By.XPATH, '//*[@id="signin-recaptcha"]/div/div[2]/div[2]').text
            if ("ена" in find_check) or ("lve" in find_check):
                click(driver, 40, '//button[@data-testid="final-login-button"]')
                break
            else:
                if time_loop > 120:
                    return {"status": "0", "ext": "CAPTCHA ERROR"}
                time_loop += 5
                sleep(5)
                print("Wait 5 seconds, captcha solving...")
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    sleep(5.5)
    driver.get('https://metaspins.com/casino#deposit')

    try:
        click(driver, 30, '//*[@id="modal"]/div/div/div/div[2]/div[1]/div[2]')
        click(driver, 30, '//*[@id="modal"]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/p')
    except Exception as e:
        print(f'ERROR CHOOSE SELECT TAG \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="modal"]/div/div/div/div[2]/div[2]/p[1]')
            amount = amount_elem.text.replace("Tron(TRC-20)", '')

            driver.implicitly_wait(30)
            click(driver, 30, '//button[@data-testid="currency-address"]')
            pyautogui.moveTo(270, 200)
            pyautogui.click()

            pyautogui.press('tab')
            sleep(1)
            pyautogui.press('tab')
            sleep(1)
            pyautogui.press('enter')

            sleep(3.5)
            address = pyperclip.paste()
            print(address)
            sleep(1)

            return {
                "address": address,
                "amount": amount.replace("Only send USDT to this address on the ", '').replace("network. Min deposit:", '').replace("Tron(TRC-20)", '').replace("USDT", '').replace(" ", '').replace("Tron(TRC-20)", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
