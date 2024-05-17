import pyautogui
from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'http://spinanga4894.com'
user_email = "kiracase34@gmail.com"
user_password = "Vbu7PsRg3a8K2Hf"


# CHROME CONSTANS

options = webdriver.ChromeOptions()
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
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


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
        click(driver, 30, '//*[@id="config-form"]/div[2]/table/tbody/tr[4]/td[1]/div/div[1]')
        click(driver, 30, '//*[@id="config-form"]/div[2]/table/tbody/tr[4]/td[1]/div/div[2]/div/div[2]')
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
    api_connect(driver)
    driver.get(url)

    while True:
        try:
            click(driver, 60, '/html/body/stb-root/stb-base-layout/stb-header/header/div/button[2]')
            input_data(driver, 30, '//*[@id="email"]', user_email)
            input_data(driver, 30, '//*[@id="current-password"]', user_password)
            click(driver, 30, '/html/body/div[1]/stb-overlay-container/div[2]/div/stb-login-dialog/stb-login-options/stb-stepper/div/stb-login-state-form/stb-login-steps/stb-stepper/stb-login-form/form/div[2]/button')
        except Exception as e:
            return {"status": "0", "ext": f"ERROR LOGIN \n{e}"}

        try:
            time_loop = 0
            while True:
                driver.implicitly_wait(10)
                find_check = driver.find_element(By.XPATH, '/html/body/div[1]/stb-overlay-container/div[2]/div/stb-login-dialog/stb-login-options/stb-stepper/div/stb-login-state-form/stb-login-steps/stb-stepper/stb-login-form/div/div[2]').text
                if ("ена" in find_check) or ("lve" in find_check):
                    print("skip")
                    break
                else:
                    if time_loop > 80:
                        break
                    time_loop += 5
                    sleep(5)
                    print("Wait 5 seconds, captcha solving...")
        except Exception as e:
            print(f'ERROR CHECKBOX ')

        try:
            driver.implicitly_wait(7.5)
            find_error = driver.find_element(By.XPATH, '//p[@class="dialog-header__title"]')
            error = find_error.text
            if "ps" in error:

                click(driver, 10, '/html/body/div[1]/stb-overlay-container/div[2]/div/stb-request-failed-dialog/div/div/div[2]/button')
                sleep(2.5)
                continue
            else:
                print("Succesfull")
                break
        except:
            break

    try:
        sleep(2.5)
        js_click(driver, 70, '//button[@class="balance-info balance-info--m"]')
    except Exception as e:
        print(f'ERROR CLICK DEPOS BUT \n{e}')

    sleep(8.5)
    shadow_root = driver.find_element(By.CSS_SELECTOR, 'div[id="widget"]').shadow_root

    sleep(2.5)
    driver.implicitly_wait(20)
    shadow_root.find_element(By.CSS_SELECTOR, '#react-root-container > div > div:nth-child(4) > div > button').click()

    driver.implicitly_wait(20)
    choose_trc20 = shadow_root.find_element(By.CSS_SELECTOR, 'img[alt="USDTTRONTRC20"]')
    sleep(2.5)
    driver.execute_script("arguments[0].click();", choose_trc20)


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        try:
            sleep(2.5)
            shadow_root = driver.find_element(By.CSS_SELECTOR, 'div[id="widget"]').shadow_root

            driver.implicitly_wait(10)
            amount = shadow_root.find_element(By.CSS_SELECTOR, '#react-root-container > div > div:nth-child(4) > div > div > div > input').get_attribute('min')
            print(amount)

            driver.implicitly_wait(10)
            shadow_root.find_element(By.CSS_SELECTOR, '#react-root-container > div > div:nth-child(4) > div > div > button').click()

            driver.implicitly_wait(10)
            get_src = shadow_root.find_element(By.CSS_SELECTOR, '#react-root-container > div > div:nth-child(4) > div > iframe').get_attribute('src')
            driver.get(get_src)

            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//div[@class="wallet-address"]')
            address = address_elem.text

            return {
                "address": address,
                "amount": int(amount) / 23,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)


if __name__ == "__main__":
    wallet()
