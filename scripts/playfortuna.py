import asyncio
from twocaptcha.solver import TwoCaptcha
import pyperclip
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://playfortuna.com/en'
user_email = "kiracase34@gmail.com"
user_password = "_Rs_NG57T#45rj!"
site_key = '6LehO6IUAAAAAIF3MAXtAwivxYJ7n5l5mFT3RP8C'

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
    ext = paths[1].strip()
    api_key = paths[3].strip()

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

    # input("press")
    #
    # handles = await driver.window_handles
    # for handle in handles:
    #     await asyncio.sleep(1)
    #     await driver.switch_to.window(handle)
    #     title = await driver.title
    #     print(title)
    #     if "2Cap" in title:
    #         break
    #
    # try:
    #     await asyncio.sleep(2.5)
    #     await input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
    #     await click(driver, 30, '//*[@id="connect"]')
    # except Exception as e:
    #     print(f'ERROR CONNECT \n{e}')
    #
    # handles = await driver.window_handles
    # print(handles)
    # for handle in handles:
    #     await driver.switch_to.window(handle)
    #     title = await driver.title
    #     if "Pla" in title:
    #         break

    try:
        await click(driver, 70, '/html/body/div[2]/header/div/div/div[4]/span')
        await input_data(driver, 30, '//*[@id="login_login"]', user_email)
        await input_data(driver, 30, '//*[@id="login_passwordPlain"]', user_password)

        await asyncio.sleep(10)
        solver = TwoCaptcha(api_key)
        print("Start solve captcha...")

        result = solver.recaptcha(sitekey=site_key, url=url)
        print(f"РЕЗУЛЬТАТ: {str(result['code'])}")

        input_captcha_code = await driver.find_element(By.TAG_NAME, 'textarea', timeout=10)
        await driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result['code'])

    except Exception as e:
        print(f"ERROR INPUT LOG DATA \n{e}")

    try:
        await click(driver, 50, '//*[@id="login-form-js"]/div/div[5]/button')
    except Exception as e:
        print(f'ERROR CLICK SOLVE BUT \n{e}')

    while True:
        try:
            await asyncio.sleep(10)
            find_error = await driver.find_element(By.XPATH, '//div[@data-error="recaptcha"]', timeout=10)
            error_text = await find_error.text
            if "fail" in error_text:
                await asyncio.sleep(10)
                solver = TwoCaptcha(api_key)
                print("Start solve captcha...")

                result = solver.recaptcha(sitekey=site_key, url=url)
                print(f"РЕЗУЛЬТАТ: {str(result['code'])}")

                input_captcha_code = await driver.find_element(By.TAG_NAME, 'textarea', timeout=10)
                await driver.execute_script("arguments[0].innerHTML = arguments[1]", input_captcha_code, result['code'])

                try:
                    await click(driver, 30, '//*[@id="login-form-js"]/div/div[5]/button')
                except Exception as e:
                    print(f'ERROR LOG CLICK \n{e}')
            else:
                break
        except:
            break

    try:
        await asyncio.sleep(1.5)
        await click(driver, 60, '/html/body/div[2]/header/div/div/div[5]/div/a[2]')
        await asyncio.sleep(1.5)
        await click(driver, 30, '//*[@id="cash-in"]/div/div/ul/li[1]/div')
        await asyncio.sleep(1.5)
        await click(driver, 30, '//*[@id="cash-in"]/div/div/ul/li[11]/div')
    except Exception as e:
        print(f'ERROR CLICK DEPOS BUT \n{e}')

    try:
        await asyncio.sleep(1.5)
        await click(driver, 30, '//*[@id="tab-bonuses"]/div[2]/div/div/div[3]/div/div/div')
        await asyncio.sleep(1.5)
        await click(driver, 30, '//*[@id="cash-in"]/div/div/div[2]/div/div[2]/div/div/div[3]/button')
    except Exception as e:
        print(f'ERROR CHOOSE NOT BONUS \n{e}')

    try:
        await click(driver, 30, '//*[@id="tab-amount"]/div/div[2]/div[1]')
        await asyncio.sleep(1.5)
        await click(driver, 30, '//*[@id="cash-in"]/div/div/div[2]/div/div[2]/div/div/div[3]/button')
    except Exception as e:
        print(f'ERROR CHOOSE MIN AMOUNT \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await asyncio.sleep(10.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="tab-crypto-submit"]/div/div[1]/div[2]/span[1]', timeout=30)
            amount = await address_elem.text

            await click(driver, 30, '//*[@id="tab-crypto-submit"]/div/div[2]/div[2]/div[2]/button')
            await asyncio.sleep(2.5)
            address = pyperclip.paste()

            return {
                "address": address,
                "amount": amount.replace("\n", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
