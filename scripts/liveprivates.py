from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://www.liveprivates.com/ru/auth/login'
user_name = "Spongegege12"
user_email = "yewoxo4550@otemdi.com"
user_password = "Qwerty62982"

# CHROME CONSTANS

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
    except Exception as e:
        print(f"ERROR ACCEPT COOKIE \n{e}")

    try:
        input_data(driver, 30, '//*[@id="login"]/form/div[1]/input', user_name)
        sleep(1.5)
        input_data(driver, 30, '//*[@id="login"]/form/div[2]/input', user_password)
    except Exception as e:
        print(f"ERROR INPUT EMAIL \n{e}")

    try:
        sleep(2.5)
        click(driver, 30, '//*[@id="login"]/form/div[3]/button')
    except Exception as e:
        print(f"ERROR SUBMIT \n{e}")

    sleep(2.5)
    driver.get('https://www.liveprivates.com/ru/free/payment')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            click(driver, 40, '//*[@id="overlay-container"]/section/div/div[2]/div[3]/p/span/a')
        except Exception as e:
            print(f"ERROR CHOOSE LINK \n{e}")

        try:
            driver.implicitly_wait(60)
            find_tags = driver.find_elements(By.TAG_NAME, 'li')

            for tag in find_tags:
                print(tag.text)
                if "криптовалют" in tag.text:
                    sleep(1.5)
                    tag.click()
                    break

            driver.implicitly_wait(30)
            pay_but = driver.find_element(By.XPATH, '//*[@id="custom-packages"]/div/div[2]/div/div/div/form[1]/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", pay_but)
        except Exception as e:
            print(f"ERROR CHOOSE CRYPTO \n{e}")

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
            input_data(driver, 40, '//*[@id="__next"]/div/div/div[2]/div[1]/form/div/div[2]/input', user_email)
            sleep(1)
            click(driver, 20, '//*[@id="__next"]/div/div/div[2]/div[1]/div[2]/button')
            sleep(1)
        except Exception as e:
            print(f"ERROR INPUT EMAIL \n{e}")

        try:
            sleep(1.5)
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
