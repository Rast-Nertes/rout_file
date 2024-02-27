from time import sleep
import pyautogui
from flask import jsonify
from fake_useragent import UserAgent
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
import asyncio
#Lunu

#CONSTANS

url = 'https://iptv.online/signin'
user_login = 'kiracase34@gmail.com'
user_password = 'kirakira1'

#PROXY CONSTANS
proxy_name = 'WyS1nY'
proxy_pass = '8suHN9'
proxy_port = '8000'
proxy_ip = "196.19.121.187"



#CHROME CONSTANS

with open('config.txt') as file:
    chrome_path = file.read().strip() # Здесь укажи абсолютный путь к экзешнику хрома

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.binary_location = chrome_path

async def login(driver):
        await driver.set_single_proxy(f"http://{proxy_name}:{proxy_pass}@{proxy_ip}:{proxy_port}")
        await driver.get(url)
        await driver.maximize_window()

        try:
            input_email = await driver.find_element(By.CSS_SELECTOR, '#login-form > input[type=text]:nth-child(4)', timeout=30)
            sleep(1.5)
            await input_email.write(user_login)

            input_password = await driver.find_element(By.CSS_SELECTOR, '#login-form > input[type=password]:nth-child(6)', timeout=10)
            sleep(1.5)
            await input_password.write(user_password)
        except Exception as e:
            print(f"INPUT ERROR \n{e}")

        #Решение Клауд
        sleep(5)

        try:
            button_to_login = await driver.find_element(By.CSS_SELECTOR, '#login-form > button', timeout=20)
            sleep(1.5)
            await driver.execute_script("arguments[0].click();", button_to_login)
        except Exception as e:
            print(f"BUTTON TO LOGIN ERROR \n{e}")



async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        #Залогиниться
        sleep(10)

        await driver.get('https://iptv.online/ru/balance', timeout=50)

        try:
            freekassa_pay = await driver.find_element(By.ID, 'submit', timeout=10)
            sleep(1.5)
            await driver.execute_script("arguments[0].click();", freekassa_pay)
        except Exception as e:
            print(f"FREEKASSA ERROR \n{e}")

        window_handles = await driver.window_handles
        print(window_handles)
        sleep(5)
        await driver.switch_to.window(window_handles[0])
        sleep(5)
        await driver.switch_to.window(window_handles[1])

        try:
            choose_trc20 = await driver.find_element(By.ID, 'currency-15', timeout=20)
            sleep(1.5)
            await driver.execute_script("arguments[0].click();", choose_trc20)

            input_email_ = await driver.find_element(By.CSS_SELECTOR, 'form > div > div.sc-jbKcbu.jRVrdt.text-field-wrap > input')
            sleep(4)
            await input_email_.write(user_login)
        except Exception as e:
            print(f"ERROR CHOOSE TRC20 \n{e}")

        try:
            submit_button = await driver.find_element(By.ID, 'submit-payment')
            sleep(1.5)
            await driver.execute_script("arguments[0].click();", submit_button)
        except Exception as e:
            print(f"SUBMIT BUTTON ERROR \n{e}")

        try:
            amount_element = await driver.find_element(By.CSS_SELECTOR, 'div.sc-VigVT.sc-cBdUnI.dNKmDp > div.sc-kAzzGY.jLybqU > div:nth-child(5) > span', timeout=40)
            amount = await amount_element.text

            address_element = await driver.find_element(By.CSS_SELECTOR, 'div.sc-kAzzGY.jLybqU > div.sc-iwsKbI.sc-BngTV.sc-bFADNz.gxpDuO > div.sc-keVrkP.iCLDVv', timeout=10)
            address = await address_element.text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")

def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
