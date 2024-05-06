import asyncio
from anticaptchaofficial.imagecaptcha import *
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent

# CONSTANTS

url = 'https://secure.weltrade.com/login/authorization'
user_email = "leonidstakanov11@gmail.com"
user_password = "Qwerty17"
perfect_id = '84286029'
perfect_pass = 'kdUqfuz1'

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
options.add_extension(ext)


def captcha_solver():
    solver = imagecaptcha()
    solver.set_verbose(1)
    solver.set_key(api_key)

    captcha_text = solver.solve_and_return_solution("captcha.png")
    time.sleep(1)

    if captcha_text != 0:
        print("captcha text " + captcha_text)
    else:
        print("task finished with error " + solver.error_code)

    return captcha_text


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
        await input_data(driver, 30, '//*[@id="email"]', user_email)
        await input_data(driver, 30, '//*[@id="password"]', user_password)
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    await asyncio.sleep(3.5)

    try:
        await click(driver, 30, '//*[@id="sign-in"]')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        await asyncio.sleep(5.4)
        find_frame = await driver.find_element(By.XPATH, '//iframe[@title="текущую проверку reCAPTCHA можно пройти в течение ещё двух минут"]', timeout=10)
        await asyncio.sleep(0.6)
        iframe_doc = await find_frame.content_document
        click_checkbox = await iframe_doc.find_element(By.XPATH, '//button[@class="rc-button goog-inline-block rc-button-reload"]', timeout=20)
        await click_checkbox.click()

        while True:
            find_check = await iframe_doc.find_element(By.XPATH, '//button[@class="rc-button goog-inline-block rc-button-reload"]', timeout=10)
            if find_check:
                await asyncio.sleep(5)
                print("Wait 5 seconds, captcha solving...")
            else:
                break

    except Exception as e:
        print(f'ERROR CHECKBOX \n{e}')

    await asyncio.sleep(2.5)
    await driver.get('https://secure.weltrade.com/cashbox/operations/deposit')

    try:
        await click(driver, 10, '//*[@id="demoContest"]/div[1]/div/div[1]/button')
    except:
        pass


    try:
        choose_crypto = await driver.find_element(By.XPATH, '//*[@id="ps-Perfect Money"]', timeout=20)
        await asyncio.sleep(1.5)
        await driver.execute_script("arguments[0].click();", choose_crypto)
    except Exception as e:
        find_input_tag = await driver.find_element(By.XPATH, '//*[@id="email"]', timeout=10)
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f'ERROR CHOOSE TRC20 \n{e}')

    try:
        await input_data(driver, 30, '//*[@id="amount"]', '10')

        depos_but_click = await driver.find_element(By.XPATH, '//*[@id="deposit-btn"]', timeout=20)
        await asyncio.sleep(1.5)
        await driver.execute_script("arguments[0].click();", depos_but_click)

        await js_click(driver, 30, '//*[@id="deposit-confirm-btn"]')
    except Exception as e:
        print(f"ERROR INPUT AMOUNT \n{e}")

    try:
        await click(driver, 30, '//*[@id="r_crypto"]')
        await click(driver, 30, '//input[@name="action"]')
    except Exception as e:
        print(f'ERROR LOGIN PERFECT \n{e}')

    try:
        while True:
            try:
                find_captcha = await driver.find_element(By.XPATH, '//*[@id="f_log"]/table[1]/tbody/tr/td/table/tbody/tr[3]/td[2]/input', timeout=7.5)
            except Exception as e:
                print(f"ERROR \n{e}")
                break

            await asyncio.sleep(2.5)

            try:
                await input_data(driver, 30, '//input[@name="Login"]', perfect_id)
                await input_data(driver, 30, '//*[@id="keyboardInputInitiator0"]', perfect_pass)
            except Exception as e:
                print(f'ERROR CLICK \n{e}')

            image_captcha = await driver.find_element(By.XPATH, '//*[@id="cpt_img"]', timeout=20)
            await image_captcha.screenshot('captcha.png')

            result = captcha_solver()
            await asyncio.sleep(1.5)

            await input_data(driver, 30, '//*[@id="f_log"]/table[1]/tbody/tr/td/table/tbody/tr[3]/td[2]/input', result)
            await click(driver, 30, '//*[@id="f_log"]/table[2]/tbody/tr[2]/td[1]/input')

            await asyncio.sleep(5.5)
    except:
        pass

    try:
        await click(driver, 30, '//label[@for="USDTTRC"]')
        await click(driver, 30, '//input[@value="Сделать платеж"]')
    except Exception as e:
        print(f'ERROR MAKE PAYMENT \n{e}')


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        log = await login(driver)
        if log:
            return log

        await asyncio.sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '//*[@id="auth"]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//*[@id="auth"]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td/table[2]/tbody/tr/td/table/tbody/tr/td/div/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]', timeout=30)
            amount = await amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
