from time import sleep
import pyautogui
from flask import jsonify
from fake_useragent import UserAgent
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
import asyncio

#CONSTANS

url = 'https://endway.su/login/'
user_login = 'kiracase34@gmail.com'
user_pass = 'kirakira123'

#CHROME OPTIONS

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()

options = webdriver.ChromeOptions()
options.binary_location = chrome_path


async def login(driver):
    await driver.get(url)
    await driver.maximize_window()
    await driver.refresh()

    try:
        input_email = await driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div/div[2]/div/div/div/div/div[2]/form/div/div/dl[1]/dd/input', timeout=20)
        sleep(3)
        await input_email.write(user_login)

        input_pass = await driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/div/div[2]/div/div/div/div/div[2]/form/div/div/dl[2]/dd/div/div/input', timeout=10)
        sleep(2)
        await input_pass.write(user_pass)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")
        return "Not work input"

    try:
        click_button_to_login = await driver.find_element(By.XPATH, '//*[@id="top"]/div[3]/div/div[2]/div/div/div/div/div[2]/form/div/button', timeout=5)
        sleep(1)
        await driver.execute_script("arguments[0].click();", click_button_to_login)
    except Exception as e:
        print(f"CLICK BUTTON TO LOGIN ERROR \n{e}")
        return "Now work click button to login"


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)
        sleep(3)
        await driver.get('https://endway.su/wallet/deposit')

        try:
            choose_crypto_pay = await driver.find_element(By.CSS_SELECTOR, 'div.p-body-content > div > form > div > div > dl:nth-child(2) > dd > div > div:nth-child(2)', timeout=10)
            sleep(2)
            await driver.execute_script("arguments[0].click();", choose_crypto_pay)
        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")
            return "Not work choose"

        try:
            next_step_payment = await driver.find_element(By.CSS_SELECTOR, 'div.formSubmitRow-controls > button > span', timeout=20)
            sleep(2)
            await driver.execute_script("arguments[0].click();", next_step_payment)
        except Exception as e:
            print(f"NEXT STEP ERROR \n{e}")
            return "Not work next step button"

        try:
            await asyncio.sleep(4)
            find_frame = await driver.find_elements(By.TAG_NAME, 'iframe')
            await asyncio.sleep(0.6)
            iframe_doc = await find_frame[0].content_document
            click_checkbox = await iframe_doc.find_element(By.XPATH, '//*[@id="challenge-stage"]/div/label/input',
                                                           timeout=20)
            await click_checkbox.click()
        except Exception as e:
            print(f'ERROR CHECKBOX')

        try:
            input_email = await driver.find_element(By.XPATH, '//*[@id="payer_details"]', timeout=40)
            await asyncio.sleep(3)
            await input_email.write(user_login)

            next_step_after_input_email = await driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/form[1]/div/button', timeout=30)
            await asyncio.sleep(2)
            await driver.execute_script("arguments[0].click();", next_step_after_input_email)
        except Exception as e:
            print(f"INPUT EMAIL ERROR \n{e}")
            return "Not work input"

        try:
            choose_tether = await driver.find_element(By.XPATH, '//div[@method-name="USDTTRC"]', timeout=40)
            await asyncio.sleep(3)
            await choose_tether.click()
        except Exception as e:
            print(f"CHOOSE TETHER ERROR \n{e}")
            return "Not work choose tether"

        try:
            accept = await driver.find_element(By.XPATH,
                                               '//input[@type="button"]', timeout=30)

            await asyncio.sleep(2)
            await driver.execute_script("arguments[0].click();", accept)
        except Exception as e:
            print(f"CONTINUE BUTTON ERROR \n{e}")
            return "Not work continue button"

        try:
            amount_element = await driver.find_element(By.XPATH, '//*[@id="amount"]', timeout=30)
            amount = await amount_element.text

            address_element = await driver.find_element(By.XPATH, '//*[@id="address"]', timeout=30)
            address = await address_element.text
        except Exception as e:
            print(f"DATA ERROR \n{e}")
            return "Not work data"

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
