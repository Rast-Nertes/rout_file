from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://www.mytrannycams.com/ru/auth/login'
user_email = "yewoxo12"
user_email_2 = "yewoxo12@gmail.com"
user_password = "Qwerty62982"

# CHROME CONSTANS

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

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1)
    driver.execute_script("arguments[0].click();", elem_click)
    sleep(1)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        click(driver, 10, '//*[@id="react-app"]/div/div[2]/button')
        sleep(2.5)
    except Exception as e:
        print(f"ERROR ACCEPT COOKIE \n{e}")

    try:
        input_data(driver, 30, '//*[@id="login"]/form/div[1]/input', user_email)
        sleep(2.5)
        input_data(driver, 30, '//*[@id="login"]/form/div[2]/input', user_password)
    except Exception as e:
        print(f"ERROR INPUT EMAIL \n{e}")

    try:
        sleep(2.5)
        click(driver, 30, '//*[@id="login"]/form/div[3]/button')
    except Exception as e:
        print(f"ERROR SUBMIT \n{e}")

    while True:
        try:
            driver.implicitly_wait(5)
            find_elem = driver.find_element(By.XPATH, '//*[@id="login"]/form/div[3]/button')
            print('wait 5 seconds...')
            sleep(5)
        except Exception as e:
            print('success')
            break

    try:
        click(driver, 5, '//*[@id="react-app"]/div/div[2]/button')
    except Exception as e:
        pass

    sleep(5.5)
    driver.get('https://www.mytrannycams.com/ru/free/payment')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            click(driver, 50, '//*[@id="overlay-container"]/section/div/div[2]/div[3]/p/span/a')
        except Exception as e:
            print(f'ERROR CHOOSE PAYMENT \n{e}')

        try:
            click(driver, 40, '//*[@id="firstbill-payment-method"]/div[2]/ul/li[8]/div/form/fieldset/input[5]')
        except Exception as e:
            print(f"ERROR CHOOSE COINGATE \n{e}")

        try:
            click(driver, 40, '//*[@id="custom-packages"]/div/div[2]/div/div/div/form[1]/button/div/div[2]')
        except Exception as e:
            print(f"ERROR CHOOSE TARIFF \n{e}")

        #Coingate

        try:
            click(driver, 75, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div/label[8]')
        except Exception as e:
            print(f"ERROR CHOOSE TETHER \n{e}")

        try:
            click(driver, 25, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/button')
        except Exception as e:
            print(f"ERROR NEXT STEP ONE \n{e}")

        try:
            click(driver, 40, '//*[@id="__next"]/div/div/div[2]/div[3]/div/div/label[3]')
            sleep(1.5)
            click(driver, 30, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div[2]/div/button')
        except Exception as e:
            print(f'ERROR CHOOSE TRON NET \n{e}')

        try:
            input_data(driver, 40, '//*[@id="__next"]/div/div/div[2]/div[1]/form/div/div[2]/input', user_email_2)
            sleep(1)
            click(driver, 20, '//*[@id="__next"]/div/div/div[2]/div[1]/div[2]/button')
            sleep(1)
        except Exception as e:
            print(f"ERROR INPUT EMAIL \n{e}")


        try:
            driver.set_window_size(1000, 500)
            sleep(3.5)
            driver.implicitly_wait(60)
            amount = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/p').text.replace("USDT", '').replace(" ", '')

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
