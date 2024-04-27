from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from twocaptcha import TwoCaptcha
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://www.bitsler.com/ru/login'
user_email = "kiracase34@gmail.com"
user_password = "D_j24$cXGwG$?5g"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    api_key = paths[3].strip()

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


def captcha_solve():
    solver = TwoCaptcha(api_key)
    result_captcha = solver.normal('captcha.png')

    return result_captcha


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
        input_data(driver, 5, '//*[@id="lo-username"]', user_email)
        input_data(driver, 30, '//*[@id="lo-password"]', user_password)
        click(driver, 30, '//*[@id="modal___BV_modal_body_"]/div/div[2]/div/div[1]/form/div[3]/button')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    while True:
        try:
            driver.implicitly_wait(5)
            find_login_tag = driver.find_element(By.XPATH, '//*[@id="lo-username"]')

            if find_login_tag:

                driver.implicitly_wait(5)
                find_frame = driver.find_element(By.XPATH, '//*[@id="captchaElement-iframe-1"]')
                driver.switch_to.frame(find_frame)
                driver.find_element(By.XPATH, '//div[@class="mtcap-image"]').screenshot('captcha.png')

                print("Start solve...")
                result = captcha_solve()

                if len(result['code']) < 5:
                    captcha_result = str(result['code']) + "11111"
                    input_data(driver, 30, '//*[@id="mtcap-inputtext-1"]', captcha_result)
                    sleep(4.5)
                    continue

                print(result)
                print("Complete!")
                input_data(driver, 30, '//*[@id="mtcap-inputtext-1"]', result['code'])
                sleep(5)
        except:
            print('Solve')
            break

    sleep(2.5)
    driver.get('https://www.bitsler.com/en/deposit')

    try:
        driver.implicitly_wait(30)
        click_choose = driver.find_element(By.XPATH, '//div[@role="combobox"]')
        sleep(1.5)
        click_choose.click()

        for _ in range(21):
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.2)

        sleep(1)
        actions.send_keys(Keys.ENTER).perform()
    except Exception as e:
        driver.implicitly_wait(10)
        find_input_tag = driver.find_element(By.XPATH, '//*[@id="lo-username"]')
        print("error")
        if find_input_tag:
            return "Login error."

        print(f'ERROR CHOOSE TETHER \n{e}')

    try:
        click(driver, 30, '//*[@id="modal___BV_modal_body_"]/div/div[1]/div[2]/div[1]/div[2]/button[2]')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '//*[@id="address"]').text

            return {
                "address": address,
                "amount": "0.01",
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
