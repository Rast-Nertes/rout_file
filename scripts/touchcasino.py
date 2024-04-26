import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://touchcasino.com/en/home/login'
user_email = "kiracase34@gmail.com"
user_password = "@iX9BWHv95nb7Pu"

# CHROME CONSTANTS

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()

options.binary_location = chrome_path


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
        await click(driver, 10, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')
    except Exception as e:
        print(f'ERROR CLICK COOK \n{e}')

    try:
        await click(driver, 30, '//*[@id="root"]/div[1]/div/div[2]/button[1]')
    except Exception as e:
        print(f'ERROR CLICK LOG BUT \n{e}')

    try:
        await input_data(driver, 30, '//input[@name="email_input"]', user_email)
        await input_data(driver, 30, '//input[@name="password_input"]', user_password)
        await click(driver, 30, '//button[@type="submit"]')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        await click(driver, 30, '//button[@class="deposit-button"]')
    except Exception as e:
        print(f'ERROR CLICK DEPOS BUT \n{e}')

    try:
        await asyncio.sleep(1.5)
        await click(driver, 30, '//div[@method="cryptocurrencybitpace"]')
        await asyncio.sleep(1.5)
        await click(driver, 30, "//div[@class='deposit-amount ' and text()='€20']")
        await click(driver, 30, "//div[@class='info-title'][p='No Bonus']")
    except Exception as e:
        print(f'ERROR CHOOSE CRYPTO \n{e}')

    try:
        await click(driver, 30, "//button[@type='button' and contains(text(), 'Deposit without bonus')]")
    except Exception as e:
        print(f'ERROR DEPOS BUT \n{e}')

    try:
        find_src = await driver.find_element(By.NAME, 'transaction-container', timeout=60)
        src = await find_src.get_attribute('src')
        await asyncio.sleep(1)
        await driver.get(src)
    except Exception as e:
        print(f'ERROR GET A SRC \n{e}')

    try:
        await click(driver, 30, "//span[@class='title' and text()='Tether']")
        await click(driver, 30, '//*[@id="app"]/div/div/div/div[2]/div/ul/li[6]/div[2]/ul/li[1]/a')
        await click(driver, 30, '//*[@id="app"]/div/div/div/div[2]/div/span[2]/button')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(1.5)
        try:
            copy_address = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/ul/li[2]/div/div[3]/a', timeout=20)
            await asyncio.sleep(1)
            await copy_address.click()

            await asyncio.sleep(1.5)
            address = pyperclip.paste()

            await asyncio.sleep(3.5)

            copy_amount = await driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[2]/div/div/ul/li[1]/div/div[3]/a', timeout=20)
            await asyncio.sleep(2.5)
            await copy_amount.click()

            await asyncio.sleep(1.5)
            amount = pyperclip.paste()

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
