import selenium.webdriver.chrome.webdriver
from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://paripesa24.biz/ru/block'
user_email = "873998755"
user_password = "e3x4yw7x"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_argument('--disable-notifications')
options.add_argument('--log-level=3')
options.add_argument('--disable-remote-fonts')
options.add_experimental_option('prefs', {'intl.accept_languages': 'en, en_US'})

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
    driver.maximize_window()
    driver.get(url)

    try:
        click(driver, 45, '//*[@id="app"]/div[3]/header/div[2]/span[2]/div/div/button')
        click(driver, 30, '//*[@id="app"]/div[3]/header/div[2]/span[2]/div/div[2]/div/div/div/form/div[4]/div/button')
    except Exception as e:
        return {"status": "0", "ext": f"error click to log \n{e}"}

    try:
        sleep(2.5)
        input_data(driver, 30, '/html/body/div[1]/div/div/div[3]/header/div/span[2]/div/div[2]/div/div/div/form/div[2]/div/input', user_email)
        input_data(driver, 30, '/html/body/div[1]/div/div/div[3]/header/div[2]/span[2]/div/div[2]/div/div/div/form/div[3]/div/input', user_password)
        click(driver, 30, '//*[@id="app"]/div[3]/header/div[2]/span[2]/div/div[2]/div/div/div/form/button/span')
    except Exception as e:
        return {"status": "0", "ext": f"error login data \n{e}"}

    sleep(2.5)
    driver.get('https://paripesa24.biz/ru/office/recharge')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        driver.implicitly_wait(30)
        find_frame = driver.find_element(By.XPATH, '//*[@id="payments_frame"]')
        driver.switch_to.frame(find_frame)

        try:
            click(driver, 30, '//div[@data-rawmethod="usdttrx"]')
            click(driver, 30, '//*[@id="deposit_button"]')
        except Exception as e:
            return {"status": "0", "ext": f"error choose trc20 \n{e}"}

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//*[@id="crypto_wallet"]')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="payment_modal_container"]/div[2]/div/div[1]/span').text
            elem = amount_elem.split('USDT')[0]
            amount = ''.join(char for char in elem if (char.isdigit()) or char == ".")

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
