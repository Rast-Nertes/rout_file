import asyncio
from flask import jsonify
from anticaptchaofficial.hcaptchaproxyless import *
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

url = 'https://imgmodels.ru'
user_email = "rwork875@gmail.com"
user_password = "22194di1qpaE"

# CHROME CONSTANS

# with open('config.txt') as file:
#     paths = file.readlines()
#     chrome_path = paths[0].strip()
#     ext = paths[1].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
# options.binary_location = chrome_path
# options.add_extension(ext)


async def login(driver):
    # await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    # await asyncio.sleep(1)
    await driver.get(url, timeout=60)
    await driver.maximize_window()

    try:
        await asyncio.sleep(2.4)
        find_frame = await driver.find_elements(By.TAG_NAME, 'iframe')
        await asyncio.sleep(0.6)
        iframe_doc = await find_frame[0].content_document
        click_checkbox = await iframe_doc.find_element(By.XPATH, '//*[@id="challenge-stage"]/div/label/input', timeout=20)
        await click_checkbox.click()
    except Exception as e:
        print(f'ERROR CHECKBOX \n{e}')

    try:
        await asyncio.sleep(1.5)
        choose_pay = await driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div/div[2]/a', timeout=20)
        await asyncio.sleep(1.5)
        await choose_pay.click()

        choose_online = await driver.find_element(By.XPATH, '//*[@id="contacts-modal"]/div/div[3]/div[3]/a', timeout=20)
        await asyncio.sleep(1)
        await choose_online.click()

        choose_payok = await driver.find_element(By.XPATH, '//*[@id="pay-modal"]/div/div[2]/div[2]/a', timeout=20)
        await asyncio.sleep(1)
        await choose_payok.click()
    except Exception as e:
        print(f'ERROR CHOOSE PAYOK \n{e}')

    try:
        input_num = await driver.find_element(By.XPATH, '//*[@id="payok"]/form/input[6]', timeout=20)
        await input_num.write("+79800800801")

        input_num = await driver.find_element(By.XPATH, '//*[@id="payok"]/form/input[7]', timeout=20)
        await input_num.write(user_email)

        click_but = await driver.find_element(By.XPATH, '//*[@id="payok"]/form/input[10]', timeout=20)
        await asyncio.sleep(1)
        await click_but.click()
    except Exception as e:
        print(f'ERROR PAYOK NEXT STEP \n{e}')

    try:
        choose_trc20 = await driver.find_element(By.XPATH, '//*[@id="pay_tether_trc"]', timeout=20)
        await asyncio.sleep(1)
        await choose_trc20.click()

        make_adres = await driver.find_element(By.XPATH, '//*[@id="pay_tether_trc_generate_button"]/span', timeout=10)
        await asyncio.sleep(1)
        await make_adres.click()
    except Exception as e:
        print(f'ERROR MAKE ADRESS \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        try:
            await asyncio.sleep(2.5)
            address_elem = await driver.find_element(By.XPATH, '//*[@id="pay_way_open_form_container_tether_trc"]/div/div[1]/fieldset[2]/input', timeout=30)
            address = await address_elem.__getattribute__('value')

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="pay_way_open_tether_trc"]/div[2]/div[2]/div[2]/div[2]', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("$", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
