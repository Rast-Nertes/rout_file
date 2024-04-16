from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from anticaptchaofficial.recaptchav2proxyless import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://klubnikacasino.net/#authorization'
user_email = "rwork875@gmail.com"
user_password = "221ldaa2312L"

#221ldaa2312L

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    api_key = paths[2].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

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


def captcha_solver():
    solver = recaptchaV2Proxyless()
    solver.set_verbose(1)
    solver.set_key(api_key)
    solver.set_website_url(url)
    solver.set_website_key(site_key)
    solver.set_soft_id(0)

    g_response = solver.solve_and_return_solution()
    return g_response


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
    driver.get(url)
    driver.maximize_window()

    try:
        input_data(driver, 20, '//*[@id="__layout"]/div/div[2]/div/section/section/section[1]/section/div[1]/div[1]/div[1]/div/div/span/span/input', user_email)
        input_data(driver, 20, '//*[@id="__layout"]/div/div[2]/div/section/section/section[1]/section/div[1]/div[1]/div[2]/div/span/span/input', user_password)
        click(driver, 20, '//*[@id="__layout"]/div/div[2]/div/section/section/section[1]/section/div[2]/button')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        click(driver, 20, '//*[@id="__layout"]/div/header/div/div/div[3]/div/div/div/div/span/button')
    except Exception as e:
        print(f'ERROR INPUT \n{e}')

    try:
        click(driver, 20, '//*[@id="__layout"]/div/main/div/div/div/section/div/section/section/div/a[6]')
    except Exception as e:
        print(f'ERROR CHOOSE CRYPTO \n{e}')

    try:
        input_data(driver, 20, '//*[@id="__layout"]/div/main/div/div/div/section/div/section/section/section[2]/div[2]/form/fieldset/div[1]/div[2]/div/input', user_email)
        click(driver, 20, '//*[@id="__layout"]/div/main/div/div/div/section/div/section/section/section[2]/div[2]/form/fieldset/div[3]/div[1]/label')
        click(driver, 20, '//*[@id="__layout"]/div/main/div/div/div/section/div/section/section/section[2]/div[2]/form/div/button')
    except Exception as e:
        print(f'ERROR INPUT EMAIL \n{e}')

    sleep(2.5)
    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        print(driver.title)
        sleep(1.5)
        if "phap" in driver.title:
            break

    try:
        driver.execute_script("window.scrollBy(0, 500);")

        driver.implicitly_wait(30)
        click_sect = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/form/div[3]/div/div/div/div/div[2]/div')
        sleep(1.5)
        click_sect.click()

        sleep(0.5)
        for _ in range(6):
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.5)

        sleep(1)
        actions.send_keys(Keys.ENTER).perform()
        sleep(1)
        click(driver, 20, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/form/div[5]/div/div/label/span[1]/input')
    except Exception as e:
        print(f'ERROR TRC20 \n{e}')

    try:
        click(driver, 20, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/form/div[6]/div/button')
    except Exception as e:
        print(f'ERROR NEXT BUT \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.NAME, 'address').get_attribute('value')

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, "//h2[@data-testid='typography-payment-amount-to-pay-value']").text.replace("USDT", '')

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
