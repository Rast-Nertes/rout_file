import asyncio
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://fezbet-7139.com'
user_email = "kiracase34"
user_password = "Kiramira123!"

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
        await click(driver, 30, '//button[@popup-open="login"]')
        await input_data(driver, 30, '//input[@name="login"]', user_email)
        await input_data(driver, 30, '//input[@name="password"]', user_password)
        await click(driver, 30, '//button[@type="submit"]')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    await asyncio.sleep(2.5)
    await driver.get('https://fezbet1.com/ru/account')

    try:
        await click(driver, 10, '//button[@class="btn btn-44-yellow missed-data__btn ng-scope"]')
    except:
        pass

    try:
        await click(driver, 30, '//button[@popup-open="cashbox"]')
    except Exception as e:
        find_input_tag = await driver.find_element(By.XPATH, '//button[@popup-open="login"]', timeout=10)
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"ERROR DEPOS BUT \n{e}")

    while True:
        try:
            await click(driver, 10, '//img[@alt="USDTether TRC20"]')
            await asyncio.sleep(1.5)
            break
        except Exception as e:
            await click(driver, 10, '//div[@popup-close="popup-close"]')
            await click(driver, 10, '//button[@popup-open="cashbox"]')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        try:
            amount_elem = await driver.find_element(By.XPATH, '//div[@class="cashbox-qamount__item ng-binding" and contains(text(), "€ 50")]', timeout=30)
            amount = await amount_elem.text

            await click(driver, 30, '//div[@class="cashbox-qamount__item ng-binding" and contains(text(), "€ 50")]')
            await click(driver, 10, "//button[contains(@class, 'cashbox-form__btn') and contains(@class, 'btn') and contains(@class, 'btn-60-yellow')]")
        except Exception as e:
            print(f'ERROR AMOUNT \n{e}')

        await asyncio.sleep(10)
        wind = await driver.window_handles
        await driver.switch_to.window(wind[0])

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//div[@class="wallet-address"]', timeout=30)
            address = await address_elem.text

            return {
                "address": address,
                "amount": amount.replace("€", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
