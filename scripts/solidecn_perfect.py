import pyautogui
from flask import jsonify
from seleniumwire import webdriver
from anticaptchaofficial.imagecaptcha import *
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://solidecn.com/Account/Login?ReturnUrl=%2FDashboard'
user_email = "linahor543@mfyax.com"
user_password = "Qwerty17"
perfect_id = '84286029'
perfect_pass = 'kdUqfuz1'

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key_recap = paths[3].strip()
    api_key_anti = paths[2].strip()
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


def captcha_solver():
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(api_key_anti)

    captcha_text = solver.solve_and_return_solution("captcha.png")
    sleep(1)

    if captcha_text != 0:
        print("captcha text " + captcha_text)
    else:
        print("task finished with error " + solver.error_code)

    return captcha_text


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
        input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key_recap)
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
        input_data(driver, 30, '//*[@id="LoginUserName"]', user_email)
        input_data(driver, 30, '//*[@id="LoginPassword"]', user_password)
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

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
        click(driver, 30, '/html/body/div[1]/div/div/div/div[1]/div/div/div/form/div/div[1]/div/span/span')
        sleep(1)
        actions.send_keys(Keys.ARROW_DOWN).perform()
        sleep(1)
        actions.send_keys(Keys.ENTER).perform()
        click(driver, 30, '/html/body/div[1]/div/div/div/div[1]/div/div/div/form/div/div[2]/div/span/span')

        for _ in range(1):
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.5)

        actions.send_keys(Keys.ENTER).perform()
    except Exception as e:
        return {"status": "0", "ext": f"ERROR CHOOSE TRC20 \n{e}"}

    try:
        sleep(1.5)
        driver.implicitly_wait(20)
        click_input_tag = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/form/div/div[4]/div/div/span[1]/span/input[1]')
        sleep(1.5)
        click_input_tag.click()
        pyautogui.write('10')
        click(driver, 30, '//*[@id="deposit-button"]')
    except Exception as e:
        return {"status": "0", "ext": f"DEPOS BUT \n{e}"}

    try:
        click(driver, 30, '//*[@id="r_crypto"]')
        click(driver, 30, '//input[@name="action"]')
    except Exception as e:
        return {"status":"0", "ext":f"ERROR CHOOSE CRYPTO \n{e} "}

    try:
        while True:
            try:
                driver.implicitly_wait(10)
                find_captcha = driver.find_element(By.XPATH, '//*[@id="cpt_img"]')
            except Exception as e:
                print("Captcha not found")
                break

            sleep(2.5)

            try:
                input_data(driver, 30, '//input[@name="Login"]', perfect_id)
                input_data(driver, 30, '//*[@id="keyboardInputInitiator0"]', perfect_pass)
            except Exception as e:
                return {"status": "0", "ext": f"ERROR PERFECT LOGIN \n{e}"}

            driver.implicitly_wait(20)
            driver.find_element(By.XPATH, '//*[@id="cpt_img"]').screenshot("captcha.png")

            result = captcha_solver()
            sleep(2.5)

            input_data(driver, 30, '//*[@id="f_log"]/table[1]/tbody/tr/td/table/tbody/tr[3]/td[2]/input', result)
            click(driver, 30, '//*[@id="f_log"]/table[2]/tbody/tr[2]/td[1]/input')

            sleep(4.5)
    except Exception as e:
        print(f"ERROR SOLVE CAPTCHA \n{e}")
        pass

    try:
        click(driver, 30, '//label[@for="USDTTRC"]')
        click(driver, 30, '//*[@id="auth"]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table[2]/tbody/tr/td/table/tbody/tr/td/div/form/table[2]/tbody/tr[2]/td[1]/input')
    except Exception as e:
        return {"status": "0", "ext": f"ERROR MAKE PAYMENT \n{e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//*[@id="auth"]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]')
            address = address_elem.text

            driver.implicitly_wait(20)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="auth"]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
