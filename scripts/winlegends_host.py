import asyncio
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://winlegends.co/de/login'
user_email = "kiracase34"
user_password = "h@a8YA3LSgzmey"

#213efi237l3

# CHROME CONSTANTS

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


async def login(driver):
    await driver.maximize_window()
    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await asyncio.sleep(1)
    await driver.get(url, timeout=60)

    try:
        input_email = await driver.find_element(By.XPATH, '//*[@id="login"]', timeout=20)
        await input_email.write(user_email)

        input_password = await driver.find_element(By.XPATH, '//*[@id="password"]', timeout=20)
        await input_password.write(user_password)

        login_button = await driver.find_element(By.XPATH, '//*[@id="popupSubmit"]', timeout=20)
        await asyncio.sleep(1)
        await login_button.click()
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    await asyncio.sleep(3.5)
    await driver.get('https://winlegends.co/de/wallet/deposit')
    await asyncio.sleep(1.5)

    await driver.execute_script("window.scrollBy(0, 400);")
    await asyncio.sleep(1.5)

    try:
        choose_trc20 = await driver.find_element(By.XPATH, '//img[@alt="Tether"]', timeout=30)
        await asyncio.sleep(1)
        await driver.execute_script("arguments[0].click();", choose_trc20)
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    try:
        click_depos_but = await driver.find_element(By.XPATH, '//*[@id="walletDepositSubmit"]', timeout=20)
        await asyncio.sleep(1)
        await driver.execute_script("arguments[0].click();", click_depos_but)
    except Exception as e:
        print(f'ERROR DEPOS BUT \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(4.5)

        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="cryptoCopyButton"]', timeout=30)
            await asyncio.sleep(1)
            await address_elem.click()

            await asyncio.sleep(1)
            address = pyperclip.paste()

            await asyncio.sleep(1.5)

            copy_amount = await driver.find_element(By.XPATH, '//*[@id="cryptoModal"]/div/div[2]/div/div/div/form/div[1]/p[2]', timeout=20)
            amount = await copy_amount.text

            await asyncio.sleep(1)

            return {
                "address": address,
                "amount": amount.replace("\n", '').replace("USDTT", '').replace(' ', ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
