from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://rt.pornhubpremium.com/premium/login'
user_email = "kiracase34@gmail.com"
user_password = "KIRAmira123123!"
api_ = '7f728c25edca4f4d0e14512d756d6868'

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    extension_path = paths[1].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_extension(extension_path)

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@45.130.254.133:8000",
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

# CHROME CONSTANS


with open('config.txt') as file:
    paths = file.readlines()
    api_key = paths[3].strip()
    ext = paths[1].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_extension(ext)


def login(driver):
    api_connect(driver)
    driver.get(url)
    driver.maximize_window()

    try:
        # input("presss")

        driver.implicitly_wait(30)
        input_email = driver.find_element(By.XPATH, '//*[@id="email"]')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '//*[@id="password"]')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '//*[@id="submitLogin"]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(10)
            enter = driver.find_element(By.ID, 'closeEnterModal')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", enter)
        except Exception as e:
            print(f"ENTER ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            upgrade_link = driver.find_element(By.ID, 'premium-upgrade-link')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", upgrade_link)

            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.XPATH, '//img[@alt="usdttrc20"]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"ERROR CHOOSE TRC20 \n{e}")

        sleep(10)

        try:
            time_loop = 0
            while True:
                driver.implicitly_wait(10)
                find_check = driver.find_element(By.XPATH, '(//div[@class="captcha-solver-info"])[2]').text
                if ("ена" in find_check) or ("lve" in find_check):
                    # click(driver, 30, '//*[@id="content"]/div/div[2]/div[2]/div/form/div[4]/button')
                    break
                else:
                    if time_loop > 120:
                        return {"status": "0", "ext": "CAPTCHA ERROR"}
                    time_loop += 5
                    sleep(5)
                    print("Wait 5 seconds, captcha solving...")
        except Exception as e:
            print(f'ERROR CHECKBOX \n{e}')

        try:
            driver.implicitly_wait(10)
            submit_button = driver.find_element(By.CSS_SELECTOR, 'div > v-crypto-form > form > div.formMainContent > div.submitWrapper > input')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit_button)
            sleep(3)
        except Exception as e:
            print(f"ERROR SUBMIT BUTTON \n{e}")

        try:
            sleep(3)
            driver.refresh()
            driver.implicitly_wait(60)
            amount = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]').text.replace("USDT", '').replace(" ", '').replace("TRX", '').replace("\n", '')

            driver.implicitly_wait(30)
            address = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[1]').text

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
