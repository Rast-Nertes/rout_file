from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://bfo7pokerdom.com/auth/login'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

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


with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    ext = paths[1].strip()
    api_key = paths[3].strip()

options.add_extension(ext)


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


def wait_visibility(driver, time, XPATH):
    WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.XPATH, XPATH))
    )
    sleep(2.5)


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
    driver.get(url)
    driver.maximize_window()
    api_connect(driver)

    try:
        input_data(driver, 35, '/html/body/gg-root/gg-layout-wrapper/div/div/ng-component/main/section/ng-component/ng-component/form/section/gg-input-login/section/div/input', user_email)
        sleep(1)
        input_data(driver, 20, '/html/body/gg-root/gg-layout-wrapper/div/div/ng-component/main/section/ng-component/ng-component/form/section/gg-input-password/section/div/input', user_password)
        sleep(1)
    except Exception as e:
        return {"status":"0", "ext":f"error login data {e}"}

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
        print(f'ERROR CHECKBOX \n{e}')

    try:
        click(driver, 30, '/html/body/gg-root/gg-layout-wrapper/div/div/ng-component/main/section/ng-component/ng-component/form/section/gg-button/button/div')
    except Exception as e:
        return {"status":"0", "ext":f"error click log but {e}"}

    try:
        wait_visibility(driver, 30, '(//button[@type="button"])[1]')
        click_depos_but = driver.find_element(By.XPATH, '(//button[@type="button"])[1]')
        sleep(3.5)
        driver.execute_script("arguments[0].click();", click_depos_but)
    except Exception as e:
        return {"status":"0", "ext":f"error depos but {e}"}

    try:
        click(driver, 25, '//*[@id="329"]')
    except Exception as e:
        return {"status":"0", "ext":f"error choose trc20 {e}"}


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
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
