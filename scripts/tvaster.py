from time import sleep
from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from fake_useragent import UserAgent
import asyncio

#CONSTANS

url = "https://my.tvaster.com/clientarea.php"
user_login = 'kiracase34@gmail.com'
user_password = '3GEahNCa@L24XzF'

#CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip() # Здесь укажи абсолютный путь к экзешнику хрома

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.binary_location = chrome_path


#PROXY CONSTANS
proxy_name = 'WyS1nY'
proxy_pass = '8suHN9'
proxy_port = '8000'
proxy_ip = "196.19.121.187"


async def login(driver):
    await driver.set_single_proxy(f"http://{proxy_name}:{proxy_pass}@{proxy_ip}:{proxy_port}")
    sleep(1)
    await driver.get(url)
    await driver.maximize_window()

    try:
        input_login = await driver.find_element(By.ID, 'inputEmail', timeout=10)
        await input_login.write(user_login)

        input_password = await driver.find_element(By.ID, 'inputPassword', timeout=10)
        await input_password.write(user_password)
    except Exception as e:
        print(f"ERROR INPUT \n{e}")

    try:
        log_button = await driver.find_element(By.ID, 'login')
        sleep(1.5)
        await driver.execute_script("arguments[0].click();", log_button)
    except Exception as e:
        print(f"LOGIN BUTTON ERROR \n{e}")

    #Время зарегестрироваться
    sleep(5)


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        await driver.get('https://my.tvaster.com/cart.php?gid=1')

        try:
            add_funds = await driver.find_element(By.ID, 'product1-order-button', timeout=20)
            sleep(1.5)
            await driver.execute_script("arguments[0].click();", add_funds)
        except Exception as e:
            print(f"ADD FUNDS ERROR \n{e}")

        try:
            complete_task = await driver.find_element(By.ID, 'btnCompleteProductConfig', timeout=20)
            sleep(1.5)
            await driver.execute_script("arguments[0].click();", complete_task)
        except Exception as e:
            print(f"ERROR ADD FUNDS \n{e}")

        try:
            checkout_button = await driver.find_element(By.ID, 'checkout', timeout=10)
            sleep(1.5)
            await driver.execute_script("arguments[0].click();", checkout_button)
        except Exception as e:
            print(f"CHECK BUTTON ERROR \n{e}")

        try:
            ticket_1 = await driver.find_element(By.CSS_SELECTOR, 'div.form-group > div > label:nth-child(2)', timeout=20)
            sleep(1.5)
            await driver.execute_script("arguments[0].click();", ticket_1)

            ticket_2 = await driver.find_element(By.CSS_SELECTOR, '#iCheck-accepttos', timeout=10)
            sleep(1.5)
            await driver.execute_script("arguments[0].click();", ticket_2)
        except Exception as e:
            print(f"TICKETS ERROR \n{e}")
        try:
            complete_order_button = await driver.find_element(By.ID, 'btnCompleteOrder', timeout=10)
            sleep(1.5)
            await driver.execute_script("arguments[0].click();", complete_order_button)
        except Exception as e:
            print(f"ORDER ERROR \n{e}")

        try:
            pay_now_button = await driver.find_element(By.CSS_SELECTOR, 'div.payment-btn-container > form > input[type=submit]', timeout=10)
            sleep(3)
            await driver.execute_script("arguments[0].click();", pay_now_button)
        except Exception as e:
            print(f"PAY NOW BUTTON ERROR \n{e}")


        #sleep(10)
        sleep(10)
        try:
            choose_tether = await driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[3]/div[7]/button', timeout=20)
            sleep(3)
            await driver.execute_script("arguments[0].click();", choose_tether)

            choose_trc20 = await driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[3]/div[2]/button', timeout=10)
            sleep(1.5)
            await driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")


        try:
            amount_element = await driver.find_element(By.ID, 'step_pay__amount_payTo', timeout=10)
            amount = await amount_element.text

            address_element = await driver.find_element(By.CSS_SELECTOR, 'div.invoice__contentWr.is-white > div.invoice__content > div > div.step-pay__address', timeout=10)
            address = await address_element.text

            return {
                "address": address,
                "amount": amount.replace("\n", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
