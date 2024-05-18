from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def wait_for_element(driver, timeout, by, value):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        print(f"Timeout: Element not found with {by} = {value}")
        return None

def js_click(driver, timeout, XPATH):
    element = wait_for_element(driver, timeout, By.XPATH, XPATH)
    if element:
        driver.execute_script("arguments[0].click();", element)

def click(driver, timeout, XPATH):
    element = wait_for_element(driver, timeout, By.XPATH, XPATH)
    if element:
        element.click()

def input_data(driver, timeout, XPATH, data):
    element = wait_for_element(driver, timeout, By.XPATH, XPATH)
    if element:
        element.clear()
        element.send_keys(data)

def login(driver):
    actions = ActionChains(driver)
    driver.maximize_window()
    api_connect(driver)
    driver.get(url)

    attempt = 0
    while attempt <= 3:
        try:
            click(driver, 60, '/html/body/stb-root/stb-base-layout/stb-header/header/div/button[1]/span')
            input_data(driver, 30, '//*[@id="email"]', user_email)
            input_data(driver, 20, '//*[@id="current-password"]', user_password)
            click(driver, 20, '//button[@data-testid="btnLogin"]')
        except Exception as e:
            print(f"ERROR LOGIN \n{e}")

        try:
            time_loop = 0
            while time_loop <= 80:
                find_check = wait_for_element(driver, 10, By.XPATH, '/html/body/div[1]/stb-overlay-container/div[2]/div/stb-login-dialog/stb-login-options/stb-stepper/div/stb-login-state-form/stb-login-steps/stb-stepper/stb-login-form/div/div[2]')
                if find_check and ("ена" in find_check.text or "lve" in find_check.text):
                    print("skip")
                    break
                time_loop += 5
                sleep(5)
                print("Wait 5 seconds, captcha solving...")
        except Exception as e:
            print(f'ERROR CHECKBOX {e}')

        try:
            find_error = wait_for_element(driver, 7.5, By.XPATH, '//p[@class="dialog-header__title"]')
            if find_error and "ps" in find_error.text:
                click(driver, 10, '/html/body/div[1]/stb-overlay-container/div[2]/div/stb-request-failed-dialog/div/div/div[2]/button')
                sleep(2.5)
                attempt += 1
                continue
            else:
                print("Successful")
                break
        except Exception as e:
            print(f'ERROR AFTER LOGIN {e}')
            break

    try:
        sleep(2.5)
        js_click(driver, 70, '//button[@data-analytics-action="Balance"]')
    except Exception as e:
        return {"status": "0", "ext": f"error depos but \n{e}"}

    try:
        sleep(4.5)
        shadow_host = wait_for_element(driver, 30, By.CSS_SELECTOR, 'div[id="widget"]')
        shadow_root = shadow_host.shadow_root if shadow_host else None

        sleep(10.5)
        shadow_root.find_element(By.CSS_SELECTOR, 'button[data-testid="expand-list-button"]').click()

        sleep(2.5)
        find_trc20_image = shadow_root.find_element(By.CSS_SELECTOR, 'img[alt="USDTTRONTRC20"]')
        driver.execute_script("arguments[0].click();", find_trc20_image)
    except Exception as e:
        return {"status": "0", "ext": f"error shadow \n{e}"}

def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        try:
            sleep(4.5)
            shadow_root = wait_for_element(driver, 10, By.CSS_SELECTOR, 'div[id="widget"]').shadow_root

            amount = shadow_root.find_element(By.CSS_SELECTOR, '#react-root-container > div > div:nth-child(4) > div > div > div > input').get_attribute('min')
            print(amount)

            sleep(1.5)
            shadow_root.find_element(By.CSS_SELECTOR, '#react-root-container > div > div:nth-child(4) > div > div > button').click()

            get_src = shadow_root.find_element(By.CSS_SELECTOR, '#react-root-container > div > div:nth-child(4) > div > iframe').get_attribute('src')
            driver.get(get_src)

            address_elem = wait_for_element(driver, 30, By.XPATH, '//div[@class="wallet-address"]')
            address = address_elem.text if address_elem else "N/A"

            return {
                "address": address,
                "amount": int(amount) / 23,
                "currency": "usdt"
            }
        except Exception as e:
            return {"status": "0", "ext": f"error data \n{e}"}

def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
