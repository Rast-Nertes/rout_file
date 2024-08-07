from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://posido158.com/en/'
user_email = "kiracase34@gmail.com"
user_password = "Rby8Fpaxpn4ztJA"

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
# options.add_argument("--auto-open-devtools-for-tabs")
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
        click(driver, 30, '//*[@id="config-form"]/div[2]/table/tbody/tr[4]/td[1]/div/div[1]')
        click(driver, 30, '//*[@id="config-form"]/div[2]/table/tbody/tr[4]/td[1]/div/div[2]/div/div[2]')
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

    while True:
        try:
            js_click(driver, 30, '/html/body/stb-root/stb-layout/stb-header/header/div/stb-header-actions/div/stb-header-buttons/div/stb-button[1]/div/button')
            input_data(driver, 30, '//*[@id="input-text-control-email"]', user_email)
            input_data(driver, 30, '//*[@id="input-password-control-password"]', user_password)
            click(driver, 30, '/html/body/div[5]/div[2]/div/stb-login-dialog/stb-login-form/div/form/div/stb-button/div/button')
        except Exception as e:
            return {"status": "0", "ext": f"ERROR LOGIN \n{e}"}

        try:
            time_loop = 0
            while True:
                driver.implicitly_wait(10)
                find_check = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/stb-login-dialog/stb-login-form/div/div/div[2]').text
                if ("ена" in find_check) or ("lve" in find_check):
                    print("skip")
                    break
                else:
                    if time_loop > 40:
                        break
                    time_loop += 5
                    sleep(5)
                    print("Wait 5 seconds, captcha solving...")
        except Exception as e:
            print(f'ERROR CHECKBOX ')

        try:
            driver.implicitly_wait(4.5)
            find_error = driver.find_element(By.XPATH, '//p[@class="dialog-header__title"]')
            error = find_error.text
            if "ps" in error:

                click(driver, 10, '/html/body/div[1]/stb-overlay-container/div[2]/div/stb-request-failed-dialog/div/div/div/div[2]/button')
                sleep(2.5)
                continue
            else:
                print("Succesfull")
                break
        except:
            break

    try:
        click(driver, 10,'/html/body/stb-root/stb-layout/div/main/article/stb-missed-data-page/div/div/div/div/form/div/stb-checkbox-control/label/span[1]')
        click(driver, 10, '/html/body/stb-root/stb-layout/div/main/article/stb-missed-data-page/div/div/div/div/form/stb-button/div/button')
    except:
        pass

    try:
        sleep(3.5)
        click(driver, 50, '/html/body/stb-root/stb-layout/stb-header/header/div/stb-header-actions/div/div[2]/stb-button/div/button')
        click(driver, 30, '//img[@alt="usdtether_trc20-pgw_coinpayments_usdt_trc20"]')
        click(driver, 30, '//label[@for="cashier-amount-280"]')
    except Exception as e:
        return {"status": "0", "ext": f"choose trc20 \n{e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        try:
            driver.implicitly_wait(30)
            sleep(3.5)
            amount = driver.find_element(By.XPATH, '//*[@id="input-number-control-amount"]').get_attribute('min')

            try:
                click(driver, 30, '/html/body/div[5]/div[2]/div/stb-cashier-dialog/div/stb-external-payment-window/stb-tab-group/div/div[2]/div/form/div/div[5]/stb-button/div/button')
            except Exception as e:
                return {"status":"0", "ext":f"error depos but \n{e}"}

            sleep(4.5)
            driver.implicitly_wait(50)
            find_src = driver.find_element(By.XPATH, '/html/body/div[5]/div[2]/div/stb-cashier-dialog/div/stb-internal-payment-window/iframe').get_attribute('src')
            driver.get(find_src)

            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//div[@class="wallet-address"]')
            address = address_elem.text

            return {
                "address": address,
                "amount": int(amount) / 23,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
