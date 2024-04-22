from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://supacasi.io/account/financials/deposit'
user_email = "kiracase34@gmail.com"
user_password = "3ikQh7QPZ@e7En"

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

    try:
        input_data(driver, 20, '//input[@name="email"]', user_email)
        input_data(driver, 20, '//input[@name="password"]', user_password)
        click(driver, 20, '//button[@type="submit"]')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')
        return "Login error."

    try:
        driver.implicitly_wait(20)
        get_src_iframe = driver.find_element(By.XPATH, '//iframe[@title="MyAccount"]').get_attribute('src')
        driver.get(get_src_iframe)
    except:
        driver.implicitly_wait(10)
        find_input_tag = driver.find_element(By.XPATH, '//input[@name="email"]')
        if find_input_tag:
            return "Login error."


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return "Login error. Check script."

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            amount = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/a[11]/div/div[2]/div[1]/span[2]').text.replace('€', '').replace(" ", '').replace("\n", '')

            try:
                click(driver, 20, "//img[@alt='USDT (TRC20)']")
            except Exception as e:
                print(f'ERROR CHOOSE TRC20 \n{e}')

            driver.implicitly_wait(20)
            address = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div/div[2]/div/div/div[1]/strong').text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
