from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://321cryptocasino.com/login'
user_email = "kiracase34"
user_password = "Kiramira000"

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
    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        # print(driver.title)
        sleep(1.5)
        if "2Cap" in driver.title:
            break

    try:
        click(driver, 30, '//*[@id="autoSolveRecaptchaV2"]')
        click(driver, 30, '//*[@id="autoSolveInvisibleRecaptchaV2"]')
        input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        click(driver, 30, '//*[@id="connect"]')
        sleep(4.5)
        driver.switch_to.alert.accept()
    except Exception as e:
        print(f'ERROR CLICK \n{e}')

    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        # print(driver.title)
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
    api_connect(driver)

    driver.get(url)
    driver.maximize_window()

    while True:
        try:
            driver.implicitly_wait(30)
            find_error_text = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/p').text
            if ("connect" in find_error_text) or ("check" in find_error_text):
                driver.refresh()
                sleep(1.5)
        except:
            print("Connected")
            break

    try:
        input_data(driver, 90, '//*[@id="loginName"]', user_email)
        input_data(driver, 30, '//*[@id="loginPassword"]', user_password)
    except Exception as e:
        return {"status": "0", "ext": f'ERROR INPUT DATA \n{e}'}

    try:
        time_loop = 0
        while True:
            driver.implicitly_wait(10)
            find_check = driver.find_element(By.XPATH, '//div[@class="captcha-solver-info"]').text
            if ("ена" in find_check) or ("lve" in find_check):
                click(driver, 30, '//*[@id="content"]/div/div[2]/div[2]/div/form/div[4]/button')
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
        sleep(1.5)
        driver.implicitly_wait(30)
        click_login = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div/form/div/div[8]/button')
        sleep(1.5)
        click_login.click()
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        driver.implicitly_wait(30)
        click_depos_but = driver.find_element(By.XPATH, '//*[@id="root"]/div/header/div/div/div/div[2]/div/div[3]/div/div[1]/a')
        sleep(1.5)
        click_depos_but.click()
    except Exception as e:
        return {"status": "0", "ext": f"DEPOS BUT ERROR \n{e}"}

    try:
        click(driver, 30, '//*[@id="panel44bh-header"]')
    except Exception as e:
        return {"status": "0", "ext": f'ERROR CHOOSE TRC20 \n{e}'}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(60)
            address_elem = driver.find_element(By.XPATH, '//*[@id="panel44bh-content"]/div/div/div[1]/div[2]/div[1]/div/div/input')
            address = address_elem.get_attribute('value')

            driver.implicitly_wait(30)
            find_min = driver.find_element(By.XPATH, '//*[@id="panel44bh-header"]/div[1]/div/div[1]/p').text
            min = int(find_min.replace('Min:', '').replace('Min: 250 UBTC', '').replace(" ", '').replace("UBTC", ""))
            print(min)

            driver.implicitly_wait(10)
            find_curse = float(driver.find_element(By.XPATH, '//*[@id="panel44bh-content"]/div/div/div[1]/div[3]/div/table/tbody/tr[1]/td[3]').text.replace("USDT.TRC20", '').replace(" ", ''))

            amount = min * find_curse

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)