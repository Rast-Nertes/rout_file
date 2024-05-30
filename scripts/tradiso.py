import pyautogui
from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://my.tradiso.com/en/login'
user_email = "kejokan542@haislot.com"
user_password = "Qwerty17."

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
        js_click(driver, 60, '//*[@id="autoSolveRecaptchaV2"]')
        js_click(driver, 60, '//*[@id="autoSolveInvisibleRecaptchaV2"]')
        js_click(driver, 30, '//*[@id="autoSolveRecaptchaV3"]')
    except Exception as e:
        print(f'ERROR CLICK \n{e}')

    try:
        input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        click(driver, 30, '//*[@id="connect"]')
        sleep(4.5)
        driver.switch_to.alert.accept()
    except Exception as e:
        print(f'ERROR INPUT API KEY \n{e}')

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
        input_data(driver, 65, '//*[@id="mat-input-0"]', user_email)
        input_data(driver, 30, '//*[@id="mat-input-1"]', user_password)
        click(driver, 30, '/html/body/app-root/div/app-external-layout/div/div/main/app-login/app-default-login/app-wizard/app-view/app-auth-card/div/app-auth-card-content/app-form/form/div[1]/button')
    except Exception as e:
        return {"status": "0", "ext": f"Login error \n{e}"}

    try:
        click(driver, 50, '//button[@title="Funds"]')
        js_click(driver, 30, '//a[@title="Deposit"]')
    except Exception as e:
        return {"status": "0", "ext": f"DEPOS BUT ERROR \n{e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        depos_amount = "100"

        try:
            click(driver, 30, '//img[@alt="usdt-trx"]')
            sleep(2.5)
            input_data(driver, 30,
                       '/html/body/app-root/div/app-internal-layout/app-full-layout/mat-sidenav-container/mat-sidenav-content/div/main/div[2]/app-conversion/app-payment-wrapper/app-conversion-page/div/app-payment/app-form/form/div/section[4]/app-currency-exchange/div/app-currency-exchange-common/div[2]/form/div[1]/div[1]/div[2]/input',
                       depos_amount)
            click(driver, 30,
                  '/html/body/app-root/div/app-internal-layout/app-full-layout/mat-sidenav-container/mat-sidenav-content/div/main/div[2]/app-conversion/app-payment-wrapper/app-conversion-page/div/app-payment/app-form/form/div/section[6]/button')
        except Exception as e:
            return {"status": "0", "ext": f"ERROR CHOOSE TRC OR INPUT AMOUNT \n{e}"}

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '/html/body/app-root/div/app-internal-layout/app-full-layout/mat-sidenav-container/mat-sidenav-content/div/main/div[2]/app-conversion/app-payment-wrapper/app-conversion-page/div/app-payment-qr/mat-card/mat-card-content/div/div[2]/div[2]/span')
            address = address_elem.text

            return {
                "address": address,
                "amount": depos_amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
