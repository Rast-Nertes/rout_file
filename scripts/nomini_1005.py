import asyncio
import pyperclip
from twocaptcha import TwoCaptcha
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://nomini-1005.com'
user_email = "kiracase34"
user_password = "Adsjkfhnncsofgu89!"
#kaksejW113


# CHROME CONSTANTS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    ext = paths[1].strip()

options.binary_location = chrome_path
# options.add_extension(ext)


async def click(driver, time, XPATH):
    find_click = await driver.find_element(By.XPATH, XPATH, timeout=time)
    await asyncio.sleep(1.5)
    await find_click.click()


async def input_data(driver, time, XPATH, data):
    find_input = await driver.find_element(By.XPATH, XPATH, timeout=time)
    await find_input.clear()
    await asyncio.sleep(0.5)
    await find_input.write(data)


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    try:
        await click(driver, 30, '//a[@popup-open="login"]')
        await input_data(driver, 30, '//input[@name="login"]', user_email)
        await input_data(driver, 30, '//input[@name="password"]', user_password)
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    while True:
        try:
            find_but = await driver.find_element(By.XPATH, '//button[@translate="popup.login.btn1"]', timeout=5)
            await asyncio.sleep(1.5)
            await find_but.click()
        except:
            break

    try:
        await click(driver, 30, '//a[@popup-open="cashbox"]')
        await click(driver, 30, '//img[@alt="USDTether TRC20"]')
    except Exception as e:
        find_input_tag = await driver.find_element(By.XPATH, '//a[@popup-open="login"]', timeout=10)
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"ERROR DEPOS BUT \n{e}")


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            find_minus_amount = await driver.find_element(By.XPATH,
                                                          '//div[@class="form-num-calc is-minus icon-minus"]',
                                                          timeout=10)
            for _ in range(11):
                await asyncio.sleep(0.2)
                await find_minus_amount.click()

            await asyncio.sleep(1)

            try:
                amount_elem = await driver.find_element(By.XPATH, '//div[@class="cashbox-form__min is-cashbox-text ng-binding"]', timeout=30)
                amount_text = await amount_elem.text
                amount = str(int(amount_text.replace('Min deposit Kč ', '')) / 23.5)
                await asyncio.sleep(1.5)
            except Exception as e:
                print(f'ERROR AMOUNT \n{e}')

            try:
                await click(driver, 30, '//button[@ng-disabled="depositForm.$invalid"]')
            except Exception as e:
                print(f'ERROR CLICK DEPOS BUT \n{e}')

            await asyncio.sleep(8)
            handles = await driver.window_handles
            for handle in handles:
                await driver.switch_to.window(handle)
                title = await driver.title
                print(title)
                if "gate" in title:
                    break

            address_elem = await driver.find_element(By.XPATH, '//div[@class="wallet-address"]', timeout=30)
            address = await address_elem.text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
