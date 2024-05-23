from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'http://winolot1.com'
user_email = "kiracase34"
user_password = "YpUHibe5QwH9JTU"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--disable-save-password-bubble")
options.add_argument('--log-level=3')
options.add_argument('--disable-remote-fonts')
options.add_experimental_option('prefs', {'intl.accept_languages': 'en, en_US'})

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    ext = paths[1].strip()

# options.add_extension(ext)
# options.binary_location = chrome_path
#
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
        sleep(3.5)
        click(driver, 60, '//*[@id="header"]/div[3]/div/div[2]/div/div/button[1]')
        input_data(driver, 30, '//*[@id="login_form[username]"]', user_email)
        input_data(driver, 30, '//*[@id="login-modal-password-input"]', user_password)
        sleep(1.5)
        click(driver, 30, "//button[@class='btn btn-primary btn-block modal-submit-button']")
    except Exception as e:
        return {"status":"0", "ext":f"error login \n{e}"}

    try:
        sleep(8.5)
        click(driver, 45, '//*[@id="deposit-button"]')
    except Exception as e:
        return {"status":"0", "ext":f"error depos but \n{e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        driver.implicitly_wait(40)
        find_frame = driver.find_element(By.XPATH, '//*[@id="cashierFrame"]')
        sleep(0.6)
        driver.switch_to.frame(find_frame)
        click_checkbox = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div/div/div[4]/div/div/div/img')
        click_checkbox.click()

        try:
            driver.implicitly_wait(45)
            click_choose_walue = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div[2]/form/div/div[1]/div[1]/div/div/div[2]/div/div/div[2]')
            sleep(1.5)
            click_choose_walue.click()

            driver.implicitly_wait(30)
            click_trc20 = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div[2]/form/div/div[1]/div[1]/div/div/div[2]/div/div[2]/div/div')
            sleep(1.5)
            click_trc20.click()

            driver.implicitly_wait(30)
            click_choose_tag = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div[2]/form/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div/input')
            sleep(1.5)
            click_choose_tag.send_keys('30')

            driver.implicitly_wait(30)
            click_depos_but = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[2]/div[2]/form/div/div[2]/div[2]/button')
            sleep(1.5)
            click_depos_but.click()

        except Exception as e:
            return {"status":"0", "ext":f"error path to trc20 \n{e}"}

        sleep(4.5)
        try:
            driver.implicitly_wait(40)
            address_elem = driver.find_element(By.XPATH, '/html/body/app-root/app-crypto-payment/div/div/mat-tab-group/div/mat-tab-body[1]/div/app-with-crypto/div/div/div[2]/app-copy-input/div/span')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '/html/body/app-root/app-crypto-payment/div/div/mat-tab-group/div/mat-tab-body[1]/div/app-with-crypto/div/p/strong[2]')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace("TRC20", '').replace(" ", ""),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data \n{e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)