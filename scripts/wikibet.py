import pyautogui
from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'http://wikibet.com'
user_email = "kiracase34@gmail.com"
user_password = "wyD37QVnCRweg8h!"

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
        click(driver, 60, '//button[@title="Login"]')
        input_data(driver, 30, '//input[@name="email"]', user_email)
        input_data(driver, 30, '//input[@name="password"]', user_password)
        click(driver, 30, '/html/body/div[1]/div[3]/div/div/form/div[3]/div/button')
    except Exception as e:
        return {"status": "0", "ext": f"Error login \n{e}"}

    sleep(2.5)
    driver.get("https://www.wikibet.com/deposit")
    sleep(2.5)


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(20)
            get_src = driver.find_element(By.XPATH, '//*[@id="cashierIframe"]')
            driver.switch_to.frame(get_src)

            click(driver, 30, '//img[@class="logo-icon USDTT"]')
            input_data(driver, 30, '//input[@name="setAmount"]', '10')

            sleep(1.5)

            click(driver, 30, '//button[@class="btn cashier-button submit-button w-full false"]')

            driver.implicitly_wait(20)
            frame = driver.find_element(By.XPATH, '//*[@id="cashier"]/section/div/iframe')
            driver.switch_to.frame(frame)

            driver.implicitly_wait(65)
            address_elem = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[4]/p[4]')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[3]/h2')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("Amount", '').replace(":", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
