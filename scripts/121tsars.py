import asyncio
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://www.121tsars.com/en/account/login'
user_email = "kiracase34@gmail.com"
user_password = "ssp7MH2iw59rwVT"

# CHROME CONSTANTS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


async def login(driver):
    await driver.maximize_window()

    await driver.set_single_proxy(f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}")
    await driver.get(url, timeout=60)

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
        input_email = await driver.find_element(By.XPATH, '//*[@id="LoginF_username"]', timeout=20)
        await input_email.write(user_email)

        input_pass = await driver.find_element(By.XPATH, '//*[@id="LoginF_password"]', timeout=20)
        await input_pass.write(user_password)

        click_log = await driver.find_element(By.XPATH, '//*[@id="rFormFields"]/div[5]/input', timeout=20)
        await click_log.click()
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    await asyncio.sleep(3.5)
    await driver.get('https://www.121tsars.com/cs/finances/refill')

    try:
        click_bonuse = await driver.find_element(By.XPATH, '//*[@id="refuse-bonus-block"]/label/span', timeout=20)
        await asyncio.sleep(1)
        await click_bonuse.click()

        click_trc20 = await driver.find_element(By.XPATH, '//*[@id="pay_165"]', timeout=20)
        await asyncio.sleep(1.5)
        await click_trc20.click()
    except Exception as e:
        print(f'ERROR CLICK TRC20 \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(1.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div[2]/div/div[5]/div/div[1]/div', timeout=30)
            await asyncio.sleep(1)
            address = await address_elem.get_attribute('title')

            #Там в тексте указано 20 EUR, я решил просто в amount передать, чтобы не мучаться 
            await asyncio.sleep(1.5)
            return {
                "address": address,
                "amount": "20",
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
