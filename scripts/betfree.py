from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://betfree.pro/en/auth/sign-in/email'
user_email = "kiracase34@gmail.com"
user_password = "eW6zaUs5rkQyx8p"

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


# proxy_address = "168.80.203.135"
# proxy_login = 'zRspV7'
# proxy_password = 'KEwj3U'
# proxy_port = 8000

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

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
        sleep(1.5)
        input_data(driver, 60, '//input[@name="email"]', user_email)
        input_data(driver, 30, '//input[@name="password"]', user_password)
        click(driver, 30, '//*[@id="root"]/div/div/div/div/div[2]/div/form/div[2]/button')
    except Exception as e:
        return {"status":"0", "exr":f"error login {e}"}

    sleep(5)
    driver.get('https://betfree.pro/en?modal_type=payment_deposit&modal_params=%7B%22paymentSystem%22%3A%22cryptocurrencies%22%2C%22value%22%3A%22USDT%22%7D')

    try:
        sleep(2.5)
        click(driver, 40, '(//button[@aria-haspopup="listbox"])[5]')
        click(driver, 30, '//li[@data-key="USDTT"]')
    except Exception as e:
        return {"status": "0", "ext":f"error choose trc20 {e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/section/div[2]/div/div/div/div[3]/section/div/div/div/div')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '/html/body/div[3]/div/div/section/div[2]/div/div/div/div[4]/div[2]/div/p')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("Min.", '').replace("amount", '').replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
