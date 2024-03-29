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
#C:/Users/Acer/Desktop/py_scripts/result/ROUT_FILE/config.txt
with open('config.txt') as file:
    paths = file.readlines()
    api = paths[3].strip()

with open('config.txt') as file:
    paths = file.readlines()
    extension_path = paths[1].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_extension(extension_path)

proxy_address = "62.3.13.13"
proxy_login = '1QjtPL'
proxy_password = 'pHSyxy'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def login(driver):
    driver.get(url)
    driver.maximize_window()

    driver.switch_to.window(driver.window_handles[0])
    try:
        driver.implicitly_wait(30)
        input_api_key = driver.find_element(By.CSS_SELECTOR,
                                            'body > div > div.content > table > tbody > tr:nth-child(1) > td:nth-child(2) > input[type=text]')
        input_api_key.clear()
        input_api_key.send_keys(api)

        driver.implicitly_wait(5)
        connect = driver.find_element(By.ID, 'connect')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", connect)
    except Exception as e:
        print(f"ERROR CONNECT \n{e}")

    driver.switch_to.window(driver.window_handles[1])
    sleep(2.5)
    try:
        driver.implicitly_wait(40)
        button_login = driver.find_element(By.CSS_SELECTOR, 'nav.ga__nav-right > div > button.btn.btn-outline-pale.btn-medium')
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
        driver.implicitly_wait(50)
        click_solve_captcha = driver.find_element(By.CSS_SELECTOR, '#recaptcha-container > div > div.captcha-solver.captcha-solver_inner')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", click_solve_captcha)
    except Exception as e:
        print(f"ERROR CLICK \n{e}")

    while True:
        try:
            driver.implicitly_wait(10)
            wait_moment = driver.find_element(By.CSS_SELECTOR, '#recaptcha-container > div > div.captcha-solver.captcha-solver_inner > div.captcha-solver-info')
            if "Решается" in wait_moment.text:
                print(f"Капча решается...")
                sleep(5)
            else:
                print(f"Captcha solved!")
                break
        except:
            break

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
            join_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/aside/div[1]/div[3]/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", join_button)

            driver.implicitly_wait(30)
            join_club = driver.find_element(By.CSS_SELECTOR, 'div.modal-ds-body.modal-ds-body--background--none.modal-ds-body--size--regular > div > div.modal-ds-footer.modal-ds-footer--background--dark > div > div > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", join_club)
        except Exception as e:
            print(f"ERROR SEND \n{e}")

        try:
            driver.implicitly_wait(30)
            choose_method_text = driver.find_element(By.CSS_SELECTOR, f'div.scroll-bar-container.b5__list.ps > div:nth-child({1}) > div.b5__left > div:nth-child(2) > div.text-s14-w500').text
            if "Crypto" in choose_method_text:
                choose_method = driver.find_element(By.CSS_SELECTOR, f'div.scroll-bar-container.b5__list.ps > div:nth-child({1}) > div.b5__left > div:nth-child(2) > div.text-s14-w500')
            else:
                choose_method = driver.find_element(By.CSS_SELECTOR, f'div.scroll-bar-container.b5__list.ps > div:nth-child({2}) > div.b5__left > div:nth-child(2) > div.text-s14-w500')
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

        try:
            driver.implicitly_wait(50)
            input_email = driver.find_element(By.XPATH, '//input[@name="email"]')
            sleep(1.5)
            input_email.clear()
            input_email.send_keys(user_email)

            driver.implicitly_wait(20)
            continue_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button)

            driver.implicitly_wait(50)
            choose_tron = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[3]/div/div/label[3]/span[2]/div')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_tron)

            driver.implicitly_wait(50)
            continue_button_2 = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div[4]/div/div[2]/div/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", continue_button_2)
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
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
