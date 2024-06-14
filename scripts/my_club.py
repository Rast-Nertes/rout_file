from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from twocaptcha import TwoCaptcha
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://my.club/'
user_email = "kiracase34"
user_password = "wDxr$7sSsT8p4VL"

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    api_key_solver = paths[5].strip()
    ext = paths[1].strip()

options = webdriver.ChromeOptions()

options.add_extension(ext)
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

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

    # input("press")
    try:
        click(driver, 10, '//button[@class="modal-ds-close-icon"]')
    except:pass

    try:
        driver.implicitly_wait(40)
        button_login = driver.find_element(By.XPATH, '(//button[@type="button"])[1]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", button_login)
    except Exception as e:
        print(f"ERROR BUTTON LOGIN \n{e}")

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.ID, 'login_login_or_email')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.ID, 'login_password')
        input_password.clear()
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"ERROR INPUT DATA \n{e}")

    try:
        time_loop = 0
        while True:
            driver.implicitly_wait(10)
            find_check = driver.find_element(By.XPATH, '//div[@class="captcha-solver-info"]').text
            if ("ена" in find_check) or ("lve" in find_check):
                break
            else:
                if time_loop > 120:
                    return {"status": "0", "ext": "CAPTCHA ERROR"}
                time_loop += 5
                sleep(5)
                print("Wait 5 seconds, captcha solving...")
    except Exception as e:
        print(f'ERROR CHECKBOX')

    try:
        driver.implicitly_wait(30)
        login_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div/div[1]/form/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    try:
        driver.implicitly_wait(40)
        choose = driver.find_element(By.XPATH, '//*[@id="app"]/div/section/div/a[1]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", choose)
    except Exception as e:
        print(f'ERROR CHOOSE \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(60)
            join_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div[1]/div[2]/section/div/div[1]/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", join_button)

            driver.implicitly_wait(30)
            join_club = driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/div/div/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", join_club)
        except Exception as e:
            print(f"ERROR SEND \n{e}")

        try:
            driver.implicitly_wait(30)
            choose_method_text = driver.find_element(By.XPATH, f'//*[@id="app-portals"]/div[2]/div[2]/div/div[2]/div[1]/div[2]').text
            if "Crypto" in choose_method_text:
                choose_method = driver.find_element(By.XPATH, f'//*[@id="app-portals"]/div[2]/div[2]/div/div[2]/div[1]/div[2]')
            else:
                choose_method = driver.find_element(By.XPATH, f'//*[@id="app-portals"]/div[2]/div[2]/div/div[2]/div[1]/div[1]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_method)
        except Exception as e:
            print(f"ERROR CHOOSE METHOD \n{e}")

        try:
            sleep(10)
            driver.implicitly_wait(30)
            iframe_elem = driver.find_element(By.XPATH, '//*[@id="billingIframeWrapperID"]/iframe')
            driver.switch_to.frame(iframe_elem)
            sleep(1.5)
        except Exception as e:
            print(f"ERROR SWITCH TO FRAME \n{e}")
        # input("Press")

        try:
            driver.implicitly_wait(20)
            choose_usdt = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div/label[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_usdt)

            driver.implicitly_wait(20)
            continue_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button)
        except Exception as e:
            print(f"ERROR CHOOSE USDT \n{e}")

        driver.implicitly_wait(50)
        choose_tron = driver.find_element(By.XPATH, '//label[@data-test="Tron-currency"]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", choose_tron)

        driver.implicitly_wait(50)
        continue_button_2 = driver.find_element(By.XPATH, '//button[@data-test="continue-button"]')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", continue_button_2)

        try:
            driver.implicitly_wait(50)
            input_email = driver.find_element(By.XPATH, '//input[@name="email"]')
            sleep(1.5)
            input_email.clear()
            input_email.send_keys("kiracase34@gmail.com")

            driver.implicitly_wait(20)
            continue_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[1]/div[2]/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button)
        except Exception as e:
            print(f"ERROR CHOOSE TRON \n{e}")

        driver.set_window_size(1200, 500)

        try:
            driver.implicitly_wait(60)
            amount = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[5]/div/div[2]/div/p').text.replace("USDT", '').replace(" ", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[6]/div/div[2]/div/p').text

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
