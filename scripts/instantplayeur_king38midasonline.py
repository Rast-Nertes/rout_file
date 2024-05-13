from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://instantplayusd.casinomidas.com:3072/lobby?skinid=1&downloadid=13481741'
user_email = "rwork8755"
user_password = "123kaHq72j"

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
    driver.get(url)

    try:
        js_click(driver, 80, '//*[@id="mainViewLoginBtn"]')
        input_data(driver, 30, '//*[@id="loginFormloginFld"]', user_email)
        input_data(driver, 30, '//*[@id="loginFormPasswordFld"]', user_password)
        click(driver, 30, '//*[@id="loginFormPlayRealBtn"]')
    except Exception as e:
        return {"status": "0", "ext": f"Login error \n{e}"}

    try:
        click(driver, 30, '//*[@id="mainViewCashierBtn"]')
    except Exception as e:
        return {"status": "0", "ext": f"DEPOS BUT \n{e}"}

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
        return {"status": "0", "ext": f"ERROR FIND FRAME \n{e}"}

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
        return {"status": "0", "ext": f"ERROR INPUT MIN AMOUNT \n{e}"}


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
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
            return {"status": "0", "ext": f"ERROR DATA \n{e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
