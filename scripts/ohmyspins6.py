import asyncio
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://ohmyspins6.com/en/'
user_email = "kiracase34"
user_password = "Kiramira000"

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
    api_key = paths[2].strip()
    ext = paths[4].strip()

options.binary_location = chrome_path
# options.add_extension(ext)


async def js_click(driver, time, XPATH):
    find_click = await driver.find_element(By.XPATH, XPATH, timeout=time)
    await asyncio.sleep(1.5)
    await driver.execute_script("arguments[0].click();", find_click)


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
        await click(driver, 30, '/html/body/stb-root/stb-layout/stb-header/header/div/div[2]/stb-button[1]/div/button')
        await input_data(driver, 30, '//*[@id="input-text-control-login"]', user_email)
        await input_data(driver, 30, '//*[@id="input-password-control-password"]', user_password)
        await click(driver, 30, '//*[@id="cdk-overlay-0"]/stb-login-dialog/stb-login-form/div/div/form/div[3]/stb-button')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        await asyncio.sleep(3.5)
        await click(driver, 60, '/html/body/stb-root/stb-layout/stb-header/header/div/div[2]/stb-button/div/button')
    except Exception as e:
        find_input_tag = await driver.find_element(By.XPATH, '//input[@placeholder="E-mail"]', timeout=7.5)
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"ERROR DEPOS BUT \n{e}")

    try:
        await js_click(driver, 30, '//img[@alt="usdtether_trc20-pgw_coinpayments_usdt_trc20"]')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        amount_elem = await driver.find_element(By.XPATH, '//div[@class="cashier-tabs--min"]', timeout=30)
        amount = await amount_elem.text

        try:
            for _ in range(3):
                await click(driver, 30, '//span[@class="input-number-control__sign minus-sign"]')

            await asyncio.sleep(1.5)
            await click(driver, 30, '/html/body/stb-root/stb-layout/stb-header/header/div/stb-toolbar-app/div[1]/stb-toolbar/stb-cashier/stb-external-payment-window/div[2]/stb-tab-group/div/div[2]/div/stb-cashier-selected-payment/form/div[6]/stb-button/div/button')
        except Exception as e:
            print(f'ERROR DEPOS BUT \n{e}')

        await asyncio.sleep(10.5)
        handles = await driver.window_handles
        print(handles)
        for handle in handles:
            await driver.switch_to.window(handle)
            title = await driver.title
            if "gate" in title:
                break

        await asyncio.sleep(2.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//div[@class="wallet-address"]', timeout=30)
            address = await address_elem.text
            print(address)

            return {
                "address": address,
                "amount": amount.replace(" Minimum €", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)