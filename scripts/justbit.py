from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://justbit.io'
user_email = "rwork875@gmail.com"
user_password = "3644103Eia123"
site_key = '6LfYdxgpAAAAADxNKcoR6vzR9__brGwS98cfIhrH'

#3644103Eia123

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    ext = paths[1].strip()
    api_key = paths[3].strip()


options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
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

    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        print(driver.title)
        sleep(1.5)
        if "2Cap" in driver.title:
            break

    try:
        input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        sleep(1)
        click(driver, 20, '//*[@id="connect"]')
    except Exception as e:
        print(f'ERROR CAP CONNECT\n{e}')

    driver.switch_to.window(windows[1])

    try:
        click(driver, 20, '//*[@id="app"]/div[2]/header/div/div/div[3]/div/div/button[1]/div')
    except Exception as e:
        print(f'ERROR CLICK BUTTON \n{e}')

    try:
        input_data(driver, 30, "//input[@type='text']", user_email)
        sleep(1)
        input_data(driver, 20, "//input[@type='password']", user_password)
        sleep(1)
        click(driver, 20, '/html/body/div[5]/div[2]/div[2]/form/div[3]/div[1]/button[1]/div')
    except Exception as e:
        print(f"ERROR LOGIN \n{e}")

    try:
        click(driver, 20, '//*[@id="gRecaptcha"]/div/div[2]')
    except Exception as e:
        print(f'ERROR SOLVE CAPTCHA \n{e}')

    while True:
        try:
            driver.implicitly_wait(10)
            find_text_captha = driver.find_element(By.XPATH, '//*[@id="gRecaptcha"]/div/div[2]/div[2]').text
            sleep(2.5)
            if "Решается" in find_text_captha:
                sleep(3.5)
                print('Wait 5 sec...')
            else:
                print('Solve!')
                sleep(1.5)
                click(driver, 20, '/html/body/div[5]/div[2]/div[2]/form/div[3]/div[1]/button[1]/div')
                break
        except:
            break

    try:
        click(driver, 20, '//*[@id="app"]/div[2]/header/div/div/div[3]/div/button[1]/div')
    except Exception as e:
        print(f'ERROR DEPOS BUTTON \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options,seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address_elem = driver.find_element(By.XPATH, '/html/body/div[7]/div[2]/div[2]/div[2]/div/div[2]/div/div[3]/div[2]/div/img').get_attribute('src')
            address = address_elem.split('=')[1]

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '/html/body/div[7]/div[2]/div[2]/div[2]/div/div[2]/div/div[2]/span').text.replace("USDTT", '').replace(" ", '')

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
