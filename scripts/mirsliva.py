from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

#CONSTANS

url = 'https://mirsliva.com/login'
user_login = "kiracase34"
user_password = "zWcBvXGiA2FkD4n"

# proxy_address = "45.130.254.133"
# proxy_login = 'K0nENe'
# proxy_password = 'uw7RQ3'
# proxy_port = 8000

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    api_key_solver = paths[5].strip()
    ext = paths[1].strip()

options.add_extension(ext)


def js_click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    driver.execute_script("arguments[0].click();", elem_click)


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    elem_click.click()


def wait_visibility(driver, time, XPATH):
    WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.XPATH, XPATH))
    )
    sleep(2.5)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


def api_connect(driver):
    sleep(1.5)
    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        sleep(1.5)
        if "2Cap" in driver.title:
            break

    try:
        js_click(driver, 30, '//*[@id="autoSolveRecaptchaV2"]')
        js_click(driver, 30, '//*[@id="autoSolveInvisibleRecaptchaV2"]')
        js_click(driver, 30, '//*[@id="autoSolveRecaptchaV3"]')
        js_click(driver, 30, '//*[@id="autoSolveHCaptcha"]')

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
        if not("2Cap" in driver.title):
            break


def login(driver):
    api_connect(driver)
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[2]/div/div/form/div[1]/div/dl[1]/dd/input')
        input_email.clear()
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[2]/div/div/form/div[1]/div/dl[2]/dd/div/div/input')
        input_password.clear()
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        click_to_login = driver.find_element(By.CSS_SELECTOR, 'div.p-body-content > div > div > form > div.block-container > dl > dd > div > div.formSubmitRow-controls > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", click_to_login)
        sleep(5)
    except Exception as e:
        print(f"BUTTON ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)
        driver.get("https://mirsliva.com/account/upgrades")

        try:
            driver.implicitly_wait(10)
            button_buy = driver.find_element(By.CSS_SELECTOR, 'div.block.block-upgrade.block-upgrade--2 > div > div.block-body.block-body--main > div.block-row.block-row--pay > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", button_buy)
        except Exception as e:
            print(f"BUTTON BUY ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_payment = driver.find_element(By.CSS_SELECTOR, 'div.block.block-upgrade.block-upgrade--2.providerSelect-active > div > div.block-body.block-body--providerSelect > div:nth-child(1) > a > span')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_payment)
        except Exception as e:
            print(f"CHOOSE PAYMENT ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_currency = driver.find_element(By.CSS_SELECTOR, 'div > div.payment1__method > div.payment1__list > label:nth-child(3) > span')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_currency)
        except Exception as e:
            print(f"CHOOSE CURRENCY ERROR \n{e}")

        try:
            time_loop = 0
            while True:
                driver.implicitly_wait(10)
                find_check = driver.find_element(By.XPATH, '//div[@class="captcha-solver-info"]').text
                if ("ена" in find_check) or ("lve" in find_check):
                    click(driver, 30, '//*[@id="content"]/div/div[2]/div[2]/div/form/div[4]/button')
                    break
                else:
                    if time_loop > 120:
                        return {"status": "0", "ext": "CAPTCHA ERROR"}
                    time_loop += 5
                    sleep(5)
                    print("Wait 5 seconds, captcha solving...")
        except Exception as e:
            print(f'ERROR CHECKBOX ')

        try:
            click(driver, 10, '//button[@type="submit"]')
        except Exception as e:
            print(f'ERROR PAY BUT \n{e}')

        try:
            WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '(//button[@target="_blank"])[2]'))
            )
            sleep(10.5)
            driver.implicitly_wait(5)
            buy_button = driver.find_element(By.XPATH, '(//button[@target="_blank"])[2]')
            driver.execute_script("arguments[0].click();", buy_button)
        except Exception as e:
            print(f"BUY BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(30)
            address = driver.find_element(By.XPATH,
                                          '(//div[@class="address-clipboard flex items-center"])[1]/span').text
            driver.implicitly_wait(30)
            amount = driver.find_element(By.XPATH,
                                         '//div[@class="amount-clipboard flex items-center"]/span').text.replace("USDT", "").replace(" ", "")
            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }

        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)