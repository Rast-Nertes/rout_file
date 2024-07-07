from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
import pyperclip
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://spinarium3.com/deposit'
user_email = "kiracase34@gmail.com"
user_password = "Kiramira123"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


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
    driver.get(url)
    driver.maximize_window()


    try:
        input_data(driver, 20, '//input[@placeholder="Email"]', user_email)
        input_data(driver, 20, '//input[@placeholder="Password"]', user_password)
        sleep(1)
        try:
            click(driver, 20, '//*[@id="onesignal-slidedown-cancel-button"]')
        except:
            pass

        click(driver, 20, '/html/body/div[1]/div/div/div[6]/div/div/form/button')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    sleep(3.5)
    driver.get('https://spinarium3.com/deposit')

    # input("press")

    try:
        click(driver, 20, '//*[@id="__nuxt"]/div/div/main/div[1]/div/div[2]/div[1]/div[1]/div/div[5]')
    except:
        return {"status": "0", "ext": "Login error. Check script."}

    try:
        click(driver, 20, '//*[@id="__nuxt"]/div/div/main/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div[1]')
        click(driver, 20, '(//button[@type="button"])[8]')
    except Exception as e:
        print(f'ERROR GET ADDRESS \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(2)
            driver.implicitly_wait(60)
            address_elem = driver.find_element(By.XPATH, '//*[@id="__nuxt"]/div/div/main/div[1]/div/div[2]/div/div/div[2]/div[3]/div[2]/div/p')
            address = address_elem.text
            print(address)

            sleep(2)
            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '//*[@id="__nuxt"]/div/div/main/div[1]/div/div[2]/div/div/div[2]/div[3]/div[4]/div/p').text
            print(amount)

            return {
                "address": address,
                "amount": amount.replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
