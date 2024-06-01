from flask import jsonify
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://solidecn.com/Account/Login?ReturnUrl=%2FDashboard'
user_email = "linahor543@mfyax.com"
user_password = "Qwerty17"

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

options.add_extension(ext)
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
    "proxy": {
        "http": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def wait_visibility(driver, time, XPATH):
    WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.XPATH, XPATH))
    )
    sleep(2.5)


def api_connect(driver):
    sleep(1.5)
    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        sleep(1.5)
        if "2Cap" in driver.title:
            break

    try:
        click(driver, 30, '//*[@id="autoSolveRecaptchaV2"]')
        click(driver, 30, '//*[@id="autoSolveInvisibleRecaptchaV2"]')
        input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        click(driver, 30, '//*[@id="connect"]')
        sleep(4.5)
        driver.switch_to.alert.accept()
    except Exception as e:
        print(f'ERROR CLICK \n{e}')

    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        sleep(1.5)
        if not ("2Cap" in driver.title):
            break


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
    actions = ActionChains(driver)
    driver.maximize_window()
    api_connect(driver)
    driver.get(url)

    try:
        wait_visibility(driver, 30, '//*[@id="LoginUserName"]')
        input_data(driver, 10, '//*[@id="LoginUserName"]', user_email)
        input_data(driver, 10, '//*[@id="LoginPassword"]', user_password)
    except Exception as e:
        return {"status": "0", "ext": f"ERROR INPUT DATA \n{e}"}

    sleep(1.5)

    try:
        time_loop = 0
        while True:
            driver.implicitly_wait(10)
            find_check = driver.find_element(By.XPATH, '//div[@class="captcha-solver-info"]').text
            if ("ена" in find_check) or ("lve" in find_check):
                click(driver, 30, '//*[@id="recaptchaBindedElement0"]')
                break
            else:
                if time_loop > 120:
                    return {"status": "0", "ext": "CAPTCHA ERROR"}
                time_loop += 5
                sleep(5)
                print("Wait 5 seconds, captcha solving...")
    except Exception as e:
        print(f'ERROR CHECKBOX \n{e}')

    sleep(7.5)
    driver.get('https://solidecn.com/Dashboard/Deposit')
    sleep(2.5)

    try:
        wait_visibility(driver, 30, '(//span[@class="k-input"])[1]')
        click(driver, 10, '(//span[@class="k-input"])[1]')
        sleep(1)
        actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(1)
        actions.send_keys(Keys.ENTER).perform()
        wait_visibility(driver, 30, '(//span[@class="k-input"])[2]')
        click(driver, 10, '(//span[@class="k-input"])[2]')

        for _ in range(4):
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.5)

        actions.send_keys(Keys.ENTER).perform()
    except Exception as e:
        return {"status": "0", "ext": f"ERROR CHOOSE TRC20 \n{e}"}

    try:
        sleep(1.5)
        wait_visibility(driver, 30, '//input[@class="k-formatted-value form-control k-input"]')
        click_input_tag = driver.find_element(By.XPATH, '//input[@class="k-formatted-value form-control k-input"]')
        sleep(1.5)
        click_input_tag.send_keys("5")
        wait_visibility(driver, 30, '//*[@id="deposit-button"]')
        click(driver, 10, '//*[@id="deposit-button"]')
    except Exception as e:
        return {"status": "0", "ext": f"DEPOS BUT \n{e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//*[@id="PaymentAddress"]')
            address = address_elem.get_attribute('value')

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div.col-sm-10.text-start')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace("(5 USD)", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status": "0", "ext": f"ERROR DATA \n{e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
