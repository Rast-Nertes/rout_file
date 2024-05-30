import pyautogui
from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://betmaximus.win/ru/cashier/deposit'
user_email = "kiracase34@gmail.com"
user_password = "v!NMZF6Lak#izdX"

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
        input_data(driver, 60, '//input[@name="usernameOrEmail"]', user_email)
        input_data(driver, 30, '//input[@name="password"]', user_password)
        js_click(driver, 30, '//button[@data-testid="login-modal-submit-button"]')
    except Exception as e:
        return {"status": "0", "ext":f"error login \n{e}"}

    try:
        click(driver, 5.8, '//*[@id="__next"]/div[1]/div[3]/div/button')
    except:
        pass

    try:
        driver.implicitly_wait(20)
        find_frame = driver.find_element(By.XPATH, '//*[@id="cashierIframe"]')
        driver.switch_to.frame(find_frame)

        sleep(2.5)
        js_click(driver, 60, '/html/body/div/div/section/div/div/div[2]/div/div/div')
        input_data(driver, 30, '/html/body/div/div/section/div/div/div[2]/div/div/div[2]/div[1]/div[2]/div/input', '40')
        js_click(driver, 30, '/html/body/div/div/section/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/div/div[1]')
        js_click(driver, 30, "//div[contains(@class, 'dropdown-item') and contains(text(), 'USDTT')]")
        js_click(driver, 30, '/html/body/div/div/section/div/div/div[2]/div/div/div[2]/div[3]/button')
    except Exception as e:
        return {"status": "0", "ext": f"depos min amount error \n{e}"}

    sleep(4.5)
    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        print(driver.title)
        sleep(1.5)
        if "api" in driver.title:
            break


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(60)
            address_elem = driver.find_element(By.XPATH, '//*[@id="app"]/div/main/div/div/div/div[4]/a')
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
