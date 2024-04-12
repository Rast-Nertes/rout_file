import asyncio
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

url = 'https://coinplay.com/ru'
user_id = ''
user_email = "fikeda5775@dacgu.com"
user_password = "Qwerty62982"
#12312lkh12g213
#843989723

# CHROME CONSTANS
#
with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    ext = paths[1].strip()

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.binary_location = chrome_path
# options.add_extension(ext)


async def login():
    async with webdriver.Chrome(options=options) as driver:
        # await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
        await driver.get(url, timeout=60)
        await driver.maximize_window()

        try:
            log_ = await driver.find_element(By.XPATH, '//*[@id="fTop"]/div/div/div/div[2]/div/div[1]/div/div/div[1]/div/button', timeout=20)
            await asyncio.sleep(1)
            await log_.click()

            input_em = await driver.find_element(By.XPATH, '//*[@id="auth_id_email"]',timeout=20)
            await asyncio.sleep(1)
            await input_em.write(user_email)

            input_pas = await driver.find_element(By.XPATH, '//*[@id="auth-form-password"]', timeout=20)
            await asyncio.sleep(1)
            await input_pas.write(user_password)

            log_but = await driver.find_element(By.XPATH, '//*[@id="main-page-step-by-step-form"]/div[2]/div[2]/div[2]/div/form/button', timeout=20)
            await asyncio.sleep(1)
            await log_but.click()
        except Exception as e:
            print(f'ERROR LOGIN \n{e}')

        try:
            await asyncio.sleep(3.5)
            input_amount = await driver.find_element(By.XPATH, '//*[@id="fTop"]/div/div/div/div[2]/div/div[1]/div/div/div[1]', timeout=20)
            await asyncio.sleep(1)
            await input_amount.click()
        except Exception as e:
            print(f'ERROR INPUT AMOUNT BUT \n{e}')

        await asyncio.sleep(2.4)
        find_frame = await driver.find_elements(By.ID, 'payments_frame_popup')

        await asyncio.sleep(0.6)
        iframe_doc = await find_frame[0].content_document

        try:
            click_checkbox = await iframe_doc.find_element(By.XPATH, '//*[@id="usdttrx_1"]', timeout=20)
            await asyncio.sleep(1)
            await click_checkbox.click()
        except Exception as e:
            print(f'ERROR CHOOSE TRC20 \n{e}')

        try:
            depos_but = await iframe_doc.find_element(By.XPATH, '//*[@id="deposit_button"]', timeout=20)
            await asyncio.sleep(1)
            await depos_but.click()
        except Exception as e:
            print(f'ERROR DEPOS BUT \n{e}')

        await asyncio.sleep(4.5)
        try:
            address_elem = await iframe_doc.find_element(By.XPATH, '//*[@id="crypto_wallet"]', timeout=30)
            address = await address_elem.text

            amount_elem = await iframe_doc.find_element(By.XPATH, '//*[@id="payment_modal_container"]/div[2]/div/div[1]/span',  timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("Минимальная сумма пополнения", '').replace("USDT", '').replace(' ', ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(login())
    print(wallet_data)
    return jsonify(wallet_data)
