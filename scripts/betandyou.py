import pyautogui
from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://betandyou.com/en'
user_email = "869260631"
user_password = "wbUvNDDbLVSsD2e"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
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
        click(driver, 12, '//*[@id="modals-container"]/div/div/div[2]/div/button')
        sleep(3.5)
        click(driver, 6, '//*[@id="modals-container"]/div/div/div[2]/div/button')
    except:
        pass

    sleep(1.5)

    try:
        click(driver, 30, '//*[@id="app"]/div[3]/header/div[2]/span[3]/div/div/button')
    except Exception as e:
        return {"status":'0', "ext":f"error log button \n{e}"}

    try:
        sleep(4.5)
        input_data(driver, 30, '/html/body/div[1]/div/div/div[3]/header/div[2]/span[3]/div/div[2]/div/div/div/form/div[2]/div/input', user_email)
        input_data(driver, 30, '/html/body/div[1]/div/div/div[3]/header/div[2]/span[3]/div/div[2]/div/div/div/form/div[3]/div/input', user_password)
    except Exception as e:
        return {"status": '0', "ext": f"error input log data \n{e}"}

    sleep(1.5)

    try:
        click(driver, 30, '//*[@id="app"]/div[3]/header/div[2]/span[3]/div/div[2]/div/div/div/form/button')
    except Exception as e:
        return {"status": '0', "ext": f"error login finish button \n{e}"}

    sleep(3.5)
    driver.get('https://betandyou.com/en/office/recharge')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(15)
            find_frame = driver.find_element(By.XPATH, '//*[@id="payments_frame"]')
            sleep(0.5)
            driver.switch_to.frame(find_frame)

            try:
                click(driver, 30, '//div[@data-method="usdttrx"]')
                click(driver, 30, '//*[@id="payment_modal_container"]/div[2]/form/div[3]/div/div[1]/button')
            except Exception as e:
                print(f'ERROR FRAME \n')

            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//*[@id="crypto_wallet"]')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="payment_modal_container"]/div[2]/form/div[4]/div/div[1]/div[1]/span')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("Minimum deposit amount", "").replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
