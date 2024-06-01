from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://catsgame.fun'
user_login = "kiracase34"
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.CSS_SELECTOR,
                                          'div.col-lg-6.pl-md--2.pr-md--2.mt-sm--3 > div > form > div > div.col-lg-8.mb-2 > center > input:nth-child(1)')
        sleep(1.5)
        input_email.clear()
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR,
                                             'div.col-lg-6.pl-md--2.pr-md--2.mt-sm--3 > div > form > div > div.col-lg-8.mb-2 > center > input:nth-child(2)')
        sleep(1.5)
        input_password.clear()
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"INPUT DATA LOGIN ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        button_login = driver.find_element(By.CSS_SELECTOR,
                                           'div.col-lg-6.pl-md--2.pr-md--2.mt-sm--3 > div > form > div > div.col-lg-8.mb-2 > center > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", button_login)
    except Exception as e:
        print(f"BUTTON LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        driver.get('https://catsgame.fun/user/insert')

        try:
            driver.implicitly_wait(10)
            input_sum = driver.find_element(By.CSS_SELECTOR, 'div.col-lg-6.pl-md--2.pr-md--2.mt-sm--3 > div > main > div > div > div > div > div.row > div:nth-child(2) > form > div:nth-child(2) > input')
            sleep(1.5)
            input_sum.clear()
            input_sum.send_keys("550")

            driver.implicitly_wait(10)
            button_success = driver.find_element(By.CSS_SELECTOR, 'div.col-lg-6.pl-md--2.pr-md--2.mt-sm--3 > div > main > div > div > div > div > div.row > div:nth-child(2) > form > div:nth-child(3) > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", button_success)
        except Exception as e:
            print(f"SUCCESS ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            accept_button = driver.find_element(By.CSS_SELECTOR, 'div.col-lg-6.pl-md--2.pr-md--2.mt-sm--3 > div > main > div > div > div > div > center > div > form > input.btn.btn-success')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", accept_button)
        except Exception as e:
            print(f"ACCEPT BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.ID, 'currency-15')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_email = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[1]/div/form/div/div[2]/input')
            input_email.clear()
            input_email.send_keys(user_email)

            driver.implicitly_wait(10)
            submit = driver.find_element(By.ID, 'submit-payment')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit)
        except Exception as e:
            print(f"INPUT ERROR \n{e}")

        try:
            driver.implicitly_wait(40)
            address = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[7]/div[2]').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[5]/span').text

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
