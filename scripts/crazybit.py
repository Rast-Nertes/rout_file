import selenium.webdriver.chrome.webdriver
from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://crazybit.io/'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
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
        click(driver, 30, '/html/body/div[1]/div/div[1]/div/div/div[2]/div/div[2]/div/div[3]/div[1]/div/div/div[2]/div/span')
        click(driver, 30, '//*[@id="root"]/div/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div[3]/div/div/div[1]/div')
        click(driver, 30, '//*[@id="root"]/div/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div/ul/li[4]')
    except Exception as e:
        return {"status": "0", "ext": f"error steps to login \n{e}"}

    try:
        input_data(driver, 30, '//*[@id="root"]/div/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[1]/div[1]/div[2]/input', user_email)
        input_data(driver, 30, '//*[@id="root"]/div/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[2]/div[1]/div[2]/input', user_password)
    except Exception as e:
        return {"status": "0", "ext": f"error login \n{e}"}

    try:
        time_loop = 0
        while True:
            driver.implicitly_wait(10)
            find_check = driver.find_element(By.XPATH, '//div[@class="captcha-solver-info"]').text
            if ("ена" in find_check) or ("lve" in find_check):
                try:
                    click(driver, 30, '//*[@id="root"]/div/div[3]/div[1]/div/div/div/div/div[2]/div[2]/div/div[5]/div')
                except Exception as e:
                    return {"status": "0", "ext": f"error login click \n{e}"}
                print("skip")
                break
            else:
                if time_loop > 80:
                    break
                time_loop += 5
                sleep(5)
                print("Wait 5 seconds, captcha solving...")
    except Exception as e:
        print(f'ERROR CHECKBOX ')

    sleep(4.5)
    driver.get('https://crazybit.io/dashboard')

    try:
        sleep(4.5)
        js_click(driver, 30, '//*[@id="root"]/div/div[1]/div/div/div[4]/div/div/div[2]/div/div[3]/div[6]/div[4]/div/div[2]/div')
        click(driver, 30, '//*[@id="root"]/div/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div[1]/div/div/div[2]/ul/li[1]')
    except Exception as e:
        return {"status": "0", "ext": f"error depos trc20 \n{e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div[1]/div[2]/div/div[3]/div[2]/div')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/div/div[4]/div/div/div[2]/div[2]/div[1]/div[2]/div/ul/li[1]/span/strong')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace("(5 USD)", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
