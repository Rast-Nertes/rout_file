import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://www.casinoestrella2024.com'
user_email = "kiracase34@gmail.com"
user_password = "Kiramira123!"

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
        await asyncio.sleep(3.5)
        await click(driver, 20, '//*[@id="side-menu"]/div/div[2]/div/span[2]/a')
    except Exception as e:
        print(f'ERROR BUT TO LOG \n{e}')

    try:
        await asyncio.sleep(4.5)
        await input_data(driver, 40,'//*[@id="login-modal"]/div/div/div[2]/div/form/div[1]/input', user_email)
        await input_data(driver, 20,'//*[@id="login-modal"]/div/div/div[2]/div/form/div[3]/input', user_password)
        await click(driver, 20, '(//button[@type="submit"])[2]')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        await click(driver, 40, '//*[@id="side-menu"]/div/div[2]/span/a')
    except Exception as e:
        find_input_tag = await driver.find_element(By.XPATH, '//*[@id="login-modal"]/div/div/div[2]/div/form/div[1]/input', timeout=10)
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"ERROR DEPOS BUT \n{e}")

    try:
        await click(driver, 20, '//*[@id="deposit-modal"]/div/div/div[2]/div/div/div/div/div[2]/span')
        await click(driver, 20, '//*[@id="deposit-modal"]/div/div/div[2]/div/div/div/div/div[1]/div[7]/span')
        await click(driver, 20, '//*[@id="deposit-modal"]/div/div/div[2]/div/div/form/div[1]/button[1]')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        try:
            amount_elem = await driver.find_element(By.XPATH, '//*[@id="deposit-modal"]/div/div/div[2]/div/div/form/div[1]/button[1]', timeout=30)
            amount = await amount_elem.text
            try:
                await click(driver, 20, '//*[@id="deposit-modal"]/div/div/div[2]/div/div/form/div[3]/button')
            except Exception as e:
                print(f'ERROR CLICK DEPOS BUT \n{e}')

            await asyncio.sleep(6)
            find_frame = await driver.find_elements(By.XPATH, '//*[@id="deposit-modal"]/div/div/div[2]/div/div/iframe')
            await asyncio.sleep(0.6)
            iframe_doc = await find_frame[0].content_document

            address_elem = await iframe_doc.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div/div/div[3]/img', timeout=60)
            await asyncio.sleep(4.5)
            address_src = await address_elem.get_attribute('src')

            parts = address_src.split(":")
            address_step_2 = parts[2]

            await asyncio.sleep(1.5)
            address = address_step_2.split("&")[0]
            await asyncio.sleep(1.5)

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
