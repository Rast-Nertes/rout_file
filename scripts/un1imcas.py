import asyncio
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://un1imcas.com/payments'
user_email = "kiracase34@gmail.com"
user_password = "48GGwwPd9s7keZu"

#4h12l312l4L2

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
    await find_input.write(data)


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    try:
        await click(driver, 40, '//*[@id="vue-integration"]/div/div[2]/div[1]/div/div/div[2]/div/table/tbody/tr[5]/td[6]/div/button')
    except Exception as e:
        print(f"ERROR CLICK LOG \n{e}")

    try:
        await input_data(driver, 30, '//*[@id="email"]', user_email)
        await input_data(driver, 20, '//*[@id="password"]', user_password)
        await asyncio.sleep(2.5)
        await click(driver, 30, '/html/body/div[6]/div[2]/div/div[1]/div/div[2]/div[2]/div/form/footer/div/button')
        await asyncio.sleep(2.5)
        await click(driver, 30, '/html/body/div[6]/div[2]/div/div[1]/div/div[2]/div[2]/div/form/footer/div/button')
    except Exception as e:
        print(f'ERROR LOG \n{e}')

    try:
        await click(driver, 20, '//*[@id="vue-integration"]/div/div[2]/div[1]/div/div/div[2]/div/table/tbody/tr[5]/td[6]/div/a/button/span')
    except Exception as e:
        find_input_tag = await driver.find_element(By.XPATH,
                                                   '//*[@id="email"]',
                                                   timeout=10)
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"ERROR DEPOS BUT \n{e}")

    try:
        await click(driver, 20, '//*[@id="personal-container"]/div/div[1]/div/div[1]/div[2]/div[6]')
    except Exception as e:
        print(f"ERROR CHOOSE TRC20 \n{e}")


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(10.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="personal-container"]/div/div[2]/div[1]/div/div[1]/div/span', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="personal-container"]/div/div[1]/div/div[2]/span', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("Количество | min ", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
