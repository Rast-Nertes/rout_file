import asyncio

from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent


# CONSTANS

url = 'https://cheatrise.com/games/eft/spoofer'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.binary_location = chrome_path


async def login(driver):
    await driver.get(url)
    await driver.maximize_window()


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)
        sleep(3)

        try:
            buy_button = await driver.find_element(By.XPATH, '/html/body/main/div/div[2]/div[2]/div/button', timeout=20)
            await driver.execute_script("arguments[0].click();", buy_button)
        except Exception as e:
            print(f"ERROR BUY BUTTON \n{e}")

        try:
            input_email = await driver.find_element(By.ID, 'purchases-email', timeout=20)
            await input_email.write(user_email)

            choose_selix = await driver.find_element(By.CSS_SELECTOR, 'div.data-row.payment-method > div.pay-sellix.linear-gradient-border.purple', timeout=20)
            await driver.execute_script("arguments[0].click();", choose_selix)
        except Exception as e:
            print(f"ERROR CHOOSE SELIX \n{e}")

        try:
            find_frame = await driver.find_elements(By.TAG_NAME, 'iframe', timeout = 10)
            sleep(2)
            iframe_document = find_frame[0].content_document

            checkbox = await iframe_document.find_element(By.XPATH, '//input[@type="checkbox"]', timeout=20)
            sleep(1.5)
            driver.execute_script("arguments[0].click();", checkbox)
        except Exception as e:
            print(f"ERROR CHECKBOX \n{e}")

        try:
            choose_usdt = await driver.find_element(By.XPATH, '//*[@id="gateway-body"]/div[2]/div[1]/div[3]/div[2]', timeout=20)
            await driver.execute_script("arguments[0].click();", choose_usdt)

            choose_trc = await driver.find_element(By.XPATH, '//*[@id="gateway-body"]/div[2]/div[1]/div[3]/div[2]/div[2]/div[3]', timeout=20)
            await driver.execute_script("arguments[0].click();", choose_trc)

            continue_button = await driver.find_element(By.CSS_SELECTOR, '#gateway-footer > div > button', timeout=20)
            await driver.execute_script("arguments[0].click();", continue_button)
        except Exception as e:
            print(f"ERROR CHOOSE TRC20 \n{e}")

        sleep(2)
        try:
            details = await driver.find_element(By.XPATH, '//*[@id="embed-body"]/div/div[1]/div[6]/div[2]/div[1]', timeout=20)
            sleep(1.5)
            await driver.execute_script("arguments[0].click();", details)
        except Exception as e:
            print(f"ERROR DETAILS \n{e}")

        sleep(3)
        try:
            address_elem = await driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[6]/div[2]/div[2]/div/div[2]/span[2]/div/div[2]/span', timeout=20)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[6]/div[2]/div[2]/div/div[2]/span[1]/div/div[2]/span')
            amount = await amount_elem.text
        except Exception as e:
            print(f"ERROR DATA \n{e}")

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
