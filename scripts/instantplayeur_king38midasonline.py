import pyautogui
from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://instantplayusd.casinomidas.com:3072/lobby?skinid=1&downloadid=13481741'
user_email = "rwork8755"
user_password = "123kaHq72j"

#123kaHq72j
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

# options.add_extension(ext)
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
    # api_connect(driver)
    driver.get(url)

    try:
        js_click(driver, 80, '//*[@id="mainViewLoginBtn"]')
        input_data(driver, 30, '//*[@id="loginFormloginFld"]', user_email)
        input_data(driver, 30, '//*[@id="loginFormPasswordFld"]', user_password)
        click(driver, 30, '//*[@id="loginFormPlayRealBtn"]')
    except Exception as e:
        return {"status": "0", "ext": f"Login error \n{e}"}

    # sleep(4.5)
    #
    # current_url = driver.current_url
    # print(current_url)
    #
    try:
        click(driver, 30, '//*[@id="mainViewCashierBtn"]')
    except Exception as e:
        return {"status": "0", "ext": f"DEPOS BUT \n{e}"}

    # windows = driver.window_handles
    # for win in windows:
    #     driver.switch_to.window(win)
    #     urls = driver.current_url
    #     print(urls)
    #     sleep(1.5)
    #     if current_url != urls:
    #         break
    sleep(3.5)
    driver.get('https://securentplayusd.casinomidas.com:2100/midusd/Mobile.WebSite/Handlers/Router.ashx?route=CashierHome&skinId=1#/cashier')

    sleep(2.5)
    driver.refresh()
    sleep(1.5)

    try:
        driver.implicitly_wait(60)
        find_frame = driver.find_element(By.XPATH, '//*[@id="deposit_Frame"]')
        driver.switch_to.frame(find_frame)
        click(driver, 30, '//*[@id="depositoptions"]/div[7]/a[2]')
    except Exception as e:
        print(f'ERROR CLICK USDT \n{e}')

    try:
        click(driver, 80, '//*[@id="CryptoNetwork"]')
        actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(0.5)
        actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()
        input_data(driver, 30, '//*[@id="chargeamount"]', "1")
        click(driver, 30, '//*[@id="SubmitBtn"]')
    except Exception as e:
        print(f'ERROR INPUT AMOUNT \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(60)
            address_elem = driver.find_element(By.XPATH, '//*[@id="cryptoAddress"]')
            address = address_elem.get_attribute('data-clipboard-text')

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="cryptoAmount"]')
            amount = amount_elem.get_attribute('data-clipboard-text')

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
