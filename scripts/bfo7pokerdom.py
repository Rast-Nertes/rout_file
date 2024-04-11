from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://bfo7pokerdom.com/auth/login'
# user_email = "rwork875@gmail.com"
# user_password = "0993e12kasrl2"
site_key = '6Lc9h3oUAAAAAIVlZ8EWCx1ycpVDxAS8WKYV0mYO'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

#0993e12kasrl2

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

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

#C:/Users/Acer/Desktop/py_scripts/result/ROUT_FILE/config.txt
with open('C:/Users/Acer/Desktop/py_scripts/result/ROUT_FILE/config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    ext = paths[1].strip()
    api_key = paths[3].strip()

options.add_extension(ext)


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
    driver.get(url)
    driver.maximize_window()

    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        print(driver.title)
        sleep(1.5)
        if "2Cap" in driver.title:
            break

    try:
        input_data(driver, 20, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        sleep(1)
        click(driver, 20, '//*[@id="connect"]')
    except Exception as e:
        print(f'ERROR CAP CONNECT\n{e}')

    driver.switch_to.window(windows[1])
    sleep(2.5)

    try:
        input_data(driver, 35, '/html/body/gg-root/gg-layout-wrapper/div/div/ng-component/main/section/ng-component/ng-component/form/section/gg-input-login/section/div/input', user_email)
        sleep(1)
        input_data(driver, 20, '/html/body/gg-root/gg-layout-wrapper/div/div/ng-component/main/section/ng-component/ng-component/form/section/gg-input-password/section/div/input', user_password)
        sleep(1)
    except Exception as e:
        print(f'ERROR DATA INPUT\n{e}')

    try:
        click(driver, 20, '//*[@id="ngrecaptcha-0"]/div/div[2]')
    except Exception as e:
        print(f'ERROR CLICK SOLVE CAPTCHA \n{e}')

    while True:
        try:
            driver.implicitly_wait(10)
            find_text_captha = driver.find_element(By.XPATH, '//*[@id="ngrecaptcha-0"]/div/div[2]/div[2]').text
            sleep(1.5)
            if "Решается" in find_text_captha:
                sleep(3.5)
                print('Wait 5 sec...')
            else:
                print('Solve!')
                sleep(1.5)
                break
        except:
            break

    try:
        click(driver, 20, '/html/body/gg-root/gg-layout-wrapper/div/div/ng-component/main/section/ng-component/ng-component/form/section/gg-button/button/div')
    except Exception as e:
        print(f'ERROR SOLVE CAPT \n{e}')

    try:
        click(driver, 40, '/html/body/gg-root/gg-layout-wrapper/div/gg-layout-header/div/div/gg-layout-header-rounded/header/div/div/gg-layout-header-deposit-button/gg-layout-deposit-button-rounded/gg-button/button/div')
    except Exception as e:
        print(f'ERROR DEPOS BUT \n{e}')

    try:
        click(driver, 25, '//*[@id="329"]')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '/html/body/gg-root/gg-layout-wrapper/div/div/ng-component/main/pd-card/section/div/pd-crypto-flow/section/div[2]/div[1]/div/div[2]/div/p').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '/html/body/gg-root/gg-layout-wrapper/div/div/ng-component/main/pd-card/section/div/pd-crypto-flow/section/div[2]/div[1]/div/div[1]/p[2]').text

            return {
                "address": address,
                "amount": amount.replace('Мин.', "").replace("депозиты :", '').replace('USDTT', '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
