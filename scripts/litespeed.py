from time import sleep
import requests
import pyautogui
from flask import jsonify
from fake_useragent import UserAgent
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import asyncio


#CAPTHCA

sitekey = '6c900d33-7534-4f65-ad7d-3727a369ddbb'
api_ = '7f728c25edca4f4d0e14512d756d6868'

#CONSTANS

url = 'https://litespeed.cc/dashboard/login'
user_login = 'kiracase34@gmail.com'
user_pass = 'LYi7BHwGJ3Xdc8D'

"""
Нужно скачать расширешение для браузера в формате (.crx) и прописать к нему путь
Ссылка на расширение: https://chrome.google.com/webstore/detail/captcha-solver-auto-recog/ifibfemgeogfhoebkmokieepdoobkbpo?hl=ru
"""
exctention_path = 'C:/Users/Acer/Desktop/py_scripts/result/bypass_captcha.crx' # Укажи здесь свой путь к расширению

#CHROME OPTIONS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_extension(exctention_path)

async def login(driver):
    await driver.get(url)
    await driver.maximize_window()

    sleep(2)
    pyautogui.moveTo(700, 300)
    pyautogui.click()
    sleep(1)

    pyautogui.write(api_)
    pyautogui.moveTo(1230, 300)
    pyautogui.click()
    sleep(2)

    await driver.switch_to.window(0)
    await driver.refresh()
    #Ждем, пока кнопка появится
    sleep(5)

    pyautogui.moveTo(420, 440)
    pyautogui.click()

    try:
        await driver.switch_to.frame(0)
        check = await driver.find_element(By.XPATH,'//*[@id="challenge-stage"]/div/label/input', timeout=3)
        sleep(1)
        await driver.execute_script("arguments[0].click();", check)
    except:
        pass

    try:
        input_email = await driver.find_element(By.ID, 'email', timeout=40)
        sleep(3)
        await input_email.write(user_login)

        input_pass = await driver.find_element(By.ID, 'password', timeout=10)
        await input_pass.write(user_pass)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")
        return jsonify("Reload Script")

    try:
        solve_hcaptcha = await driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[1]/form[1]/div[3]/div[3]/div/div/div/div/div/div[2]', timeout=10)
        sleep(1)
        await solve_hcaptcha.click()
    except Exception as e:
        print(f"SOLVE CAPTCHA ERROR \n{e}")
        return jsonify("Reload Script")


    #Решение капчи
    sleep(60)
        #return jsonify("Reload Script")

    try:
        button_to_log_in = await driver.find_element(By.CSS_SELECTOR, 'form.p-8.space-y-8.bg-white\/50.backdrop-blur-xl.border.border-gray-200.shadow-2xl.rounded-2xl.relative.filament-breezy-auth-card.dark\:bg-gray-900\/50.dark\:border-gray-700 > button')
        await driver.execute_script("arguments[0].click();", button_to_log_in)
    except Exception as e:
        print(f"BUTTON LOGIN ERROR \n{e}")
        return jsonify("Reload Script")

async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        sleep(3)
        await driver.get('https://litespeed.cc/dashboard/topup')

        try:
            click_button = await driver.find_element(By.XPATH, '//*[@id="submission"]', timeout=30)
            sleep(2)
            await driver.execute_script("arguments[0].click();", click_button)
        except Exception as e:
            print(f"CLICK BUTTON ERROR \n{e}")

        try:
            crypto_pay = await driver.find_element(By.XPATH, '//*[@id="crypto"]/span/span/span', timeout=30)
            sleep(3)
            await crypto_pay.click()
        except Exception as e:
            print(f"CRYPTO PAY ERROR \n{e}")
            return None

        try:
            choose_tether = await driver.find_element(By.XPATH,
                                                      '/html/body/div/div[2]/div[1]/div/div/div[1]/div/form/div[3]/div/button[4]',
                                                      timeout=30)
            sleep(1)
            await driver.execute_script("arguments[0].click();", choose_tether)
        except Exception as e:
            print(f"CHOOSE TETHER ERROR \n{e}")
            return None

        try:
            select_currency = await driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]', timeout=30)
            sleep(1)
            await select_currency.click()
        except Exception as e:
            print(f"SELECT ERROR \n{e}")

        try:
            choose_tether_step2 = await driver.find_element(By.XPATH, '//*[@id="downshift-2-item-0"]',timeout=10)
            sleep(1)
            await driver.execute_script("arguments[0].click();", choose_tether_step2)
        except Exception as e:
            print(f"CHOOSE TETHER STEP2 ERROR \n{e}")

        try:
            proceed_to_payment = await driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div[3]/div/button', timeout=10)
            sleep(1)
            await driver.execute_script("arguments[0].click();", proceed_to_payment)
        except Exception as e:
            print(f"PROCEED BUTTON ERROR \n{e}")

        try:
            amount_element = await driver.find_element(By.CSS_SELECTOR, 'div.payment-details__wrapper > div.payment-details__amount_wrapper > span:nth-child(1)', timeout=30)
            amount = await amount_element.text

            address_element = await driver.find_element(By.CSS_SELECTOR, 'div.checkout > div.checkout__info > div.info__recipient > div > div > span', timeout=20)
            address = await address_element.text
        except Exception as e:
            print(f"DATA ERROR \n{e}")
            return None

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }

def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)