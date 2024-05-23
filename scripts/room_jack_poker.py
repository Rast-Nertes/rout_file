from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://room.jack-poker.com/d/?tables/all'
user_email = "kiracase34"
user_password = "MXLaS7P2BSkXE2i"

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
        sleep(4.5)
        js_click(driver, 90, '//*[@id="rootUI"]/div/div[1]/div/div[1]/div/div/div/div[1]/div/div/div[2]/div/div/div/div/div/div/div[1]')
    except Exception as e:
        return {"status":"0", "ext":f"error login click:  {e}"}

    try:
        sleep(5)
        input_data(driver, 60, '//input[@name="username"]', user_email)
        input_data(driver, 40, '//input[@name="password"]', user_password)
        js_click(driver, 30, '//*[@id="rootUI"]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div/div[3]/div[2]')
    except Exception as e:
        return {"status":"0", "ext":f"error login input:  {e}"}

    try:
        sleep(4.5)
        click(driver, 40, '//*[@id="rootUI"]/div/div[1]/div/div[1]/div/div/div/div[1]/div/div/div[2]/div[1]')
        click(driver, 30, '//*[@id="rootUI"]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div/div/div/div/div/div/div/div/div[5]/div/div/div[2]/div/div/div/div/div')
    except Exception as e:
        return {"status":"0", "ext":f"error path to trc20:  {e}"}

    try:
        driver.implicitly_wait(30)
        find_frame_src = driver.find_element(By.XPATH, '//iframe[@data-cy="cashier-iframe"]')
        src = find_frame_src.get_attribute('src')
        driver.get(src)
    except Exception as e:
        return {"status":"0", "ext":f"error find src:  {e}"}

    try:
        click(driver, 50, '//div[@class="logo-container USDTT "]')
        input_data(driver, 30, '//*[@id="cashier"]/section/div/div[1]/div[2]/div/input', '10')
        sleep(2.5)
        click(driver, 30, '//*[@id="cashier"]/section/div/div[2]/button')
    except Exception as e:
        return {"status":"0", "ext":f"error input amount:  {e}"}

    sleep(4)
    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        print(driver.title)
        sleep(1.5)
        if "api" in driver.title:
            break


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(50)
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
            return {"status":"0", "ext":f"error data:  {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
