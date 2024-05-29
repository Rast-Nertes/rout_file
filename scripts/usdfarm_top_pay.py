from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://usdfarm.top/login'
user_email = "kiracase34@gmail.com"
user_password = "jHYwT@V9KH4CjyL"

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

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000


proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def wait_visibility(driver, time, XPATH):
    WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.XPATH, XPATH))
    )
    sleep(2.5)


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
        sleep(7.5)
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
            wait_visibility(driver, 60, '//input[@name="email"]')
            input_data(driver, 10, '//input[@name="email"]', user_email)
            input_data(driver, 10, '//input[@name="pass"]', user_password)
        except Exception as e:
            return {"status":"0", "ext":f"error login:  {e}"}

        try:
            time_loop = 0
            while True:
                driver.implicitly_wait(7.5)
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
            wait_visibility(driver, 30, '//button[@name="auth"]')
            js_click(driver, 10, '//button[@name="auth"]')
        except Exception as e:
            return {"status":"0", "ext":f"error click log button:  {e}"}

        try:
            wait_visibility(driver, 10, '//div[@class="alert alert-danger"]')
            find_error = driver.find_element(By.XPATH, '//div[@class="alert alert-danger"]').text

            if "ptch" in find_error:
                print('one more attempt')
                driver.refresh()
                continue
        except:
            print('skip')
            break

    sleep(2.5)
    driver.get('https://usdfarm.top/user/insert/payeer')

    try:
        sleep(3.5)
        wait_visibility(driver, 60, '//input[@type="submit"]')
        click(driver, 10, '//input[@type="submit"]')
        wait_visibility(driver, 60, '//input[@type="submit"]')
        click(driver, 10, '//input[@type="submit"]')
    except Exception as e:
        return {"status":"0", "ext":f"error depos but:  {e}"}

    try:
        wait_visibility(driver, 60, '/html/body/div/div[2]/div[3]/ul[1]/li[4]')
        click(driver, 10, '/html/body/div/div[2]/div[3]/ul[1]/li[4]')
    except Exception as e:
        return {"status":"0", "ext":f"error choose trc20:  {e}"}

    try:
        wait_visibility(driver, 60, '//*[@id="id_order_email"]')
        input_data(driver, 10, '//*[@id="id_order_email"]', user_email)
        js_click(driver, 10, '//a[@class="pay confirm-button"]')
    except Exception as e:
        return {"status":"0", "ext":f"error click buy button:  {e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            wait_visibility(driver, 60, '//*[@id="info_bitcoin"]/div[1]/h3/font[2]')
            address_elem = driver.find_element(By.XPATH, '//*[@id="info_bitcoin"]/div[1]/h3/font[2]')
            address = address_elem.text

            wait_visibility(driver, 30, '//*[@id="info_bitcoin"]/div[1]/h3/font[1]')
            amount_elem = driver.find_element(By.XPATH, '//*[@id="info_bitcoin"]/div[1]/h3/font[1]')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data:  {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)