import asyncio
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://bintrade.online/ru'
user_email = "kejokan542@haislot.com"
user_password = "Qwerty17"

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
        await click(driver, 30, '//a[@class="yellow_btn btn popup-open"]')
        await input_data(driver, 30, '//*[@id="loginform-email"]', user_email)
        await input_data(driver, 30, '//*[@id="loginform-password"]', user_password)
        await click(driver, 30, '//button[@class="yellow_btn btn form-main__submit"]')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    await asyncio.sleep(2.5)
    await driver.get('https://bintrade.online/ru/user/cash')

    try:
        await asyncio.sleep(3.5)
        await click(driver, 30, '/html/body/div[2]/div[2]/div[1]/div/div[2]/div[3]/div/div/div/div[1]/div/form/div[1]/div[2]/label[3]')
        await click(driver, 30, '//input[@class="yellow_btn filled"]')
    except Exception as e:
        find_input_tag = await driver.find_element(By.XPATH, '//*[@id="loginform-email"]', timeout=10)
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"ERROR DEPOS BUT \n{e}")

    try:
        await asyncio.sleep(3)
        find_trc20 = await driver.find_element(By.XPATH, '(//img[@alt="USDT (TRC20)"])[2]', timeout=20)
        await asyncio.sleep(1)
        await find_trc20.click()
        # await click(driver, 30, '//*[@id="currency-15"]')
        await input_data(driver, 30, '//input[@type="email"]', user_email)
        await click(driver, 30, '//*[@id="submit-payment"]')
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            amount_elem = await driver.find_element(By.XPATH, '//*[@id="pay-global"]/div/div[5]/div[1]/div[3]/div[5]/span', timeout=30)
            amount = await amount_elem.text

            address_elem = await driver.find_element(By.XPATH, '//*[@id="pay-global"]/div/div[5]/div[1]/div[3]/div[7]/div[2]', timeout=30)
            address = await address_elem.text

            return {
                "address": address,
                "amount": amount.replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
