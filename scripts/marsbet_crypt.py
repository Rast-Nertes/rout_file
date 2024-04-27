from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://www.marsbet.com/'
user_email = "kiracase34@gmail.com"
user_password = "@QWDc3xDFyc9"

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

options.binary_location = chrome_path
# options.add_extension(ext)

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

    actions = ActionChains(driver)
    try:
        click(driver, 40, '//*[@id="root"]/div/div/div[1]/div[1]/div/div[2]/header/div/div[2]/div[1]/div[1]/button')
        sleep(1.5)
        input_data(driver, 30, '//input[@name="username"]', user_email)
        sleep(1)

        try:
            driver.implicitly_wait(10)
            elem_delete = driver.find_element(By.XPATH, '//input[@name="password"]')
            driver.execute_script("arguments[0].removeAttribute('readonly');", elem_delete)
        except Exception as e:
            print(f'ERROR DELETE \n{e}')

        input_data(driver, 30, '//input[@name="password"]', user_password)
        click(driver, 30, '//button[@class="submit button"]')
    except Exception as e:
        print(f'ERROR LOG \n{e}')

    sleep(2.5)
    try:
        click(driver, 30, '//button[@class="deposit-money button"]')
    except Exception as e:
        print(f'ERROR DEPOS BUT \n{e}')
        driver.implicitly_wait(10)
        find_input_tag = driver.find_element(By.XPATH, '//input[@name="username"]')
        print("error")
        if find_input_tag:
            return "Login error."

    try:
        click(driver, 30, '//div[@class="tr payment-coinspaid"]')
        input_data(driver, 30, '//input[@name="amount"]', "10")
    except Exception as e:
        print(f'ERROR DEPOS \n{e}')

    try:
        driver.implicitly_wait(30)
        click_send_but = driver.find_element(By.CSS_SELECTOR, 'div.single-wrap > div > div.modal-content-payments-single > div > div.form-cont > form > button')
        click_send_but.click()
        click(driver, 30, '//*[@id="root"]/div/div/div[4]/div/div[2]/div/button[1]')
    except Exception as e:
        print(f'ERROR SEND BUT \n{e}')

    try:
        driver.implicitly_wait(20)
        get_src = driver.find_element(By.XPATH, "//div[@class='frame-block']/a").get_attribute('href')
        sleep(1.5)
        driver.get(get_src)
    except Exception as e:
        print(f'ERROR GO TO THE PAYMENT \n{e}')

    try:
        sleep(1.5)
        driver.implicitly_wait(30)
        select_click = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/form/div[3]/div/div/div/div')
        sleep(1.5)
        select_click.click()

        for _ in range(7):
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.5)

        actions.send_keys(Keys.ENTER).perform()

    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    try:
        click(driver, 30, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/form/div[5]/div/div/label/span[1]/input')
        click(driver, 30, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/form/div[6]/div/button')
    except Exception as e:
        print(f'ERROR CHECKBOX \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '//*[@id="mui-9"]').get_attribute('value')

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/form[1]/div[1]/div/div/div/div/div/div/div/h2').text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
