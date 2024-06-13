import asyncio

from flask import jsonify
from selenium_driverless import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent

# CONSTANS

url = 'https://chitarena.com/apex-btg#rec522496952'
user_email = "yewoxo4550@otemdi.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.binary_location = chrome_path


async def click(driver, time, XPATH):
    find_elem_click = await driver.find_element(By.XPATH, XPATH, timeout = time)
    sleep(1.5)
    await driver.execute_script("arguments[0].click();", find_elem_click)


async def login(driver):
    await driver.get(url)
    await driver.maximize_window()

    try:
        choose_tov = await driver.find_element(By.XPATH, '/html/body/div[1]/div[11]/div/div[2]/div/div/div/div[2]/div/div/div/div/div[2]/div[2]/div', timeout=30)
        sleep(1.5)
        await choose_tov.click()

        sleep(2.5)
        handles = await driver.window_handles

        for handle in handles:
            sleep(1.5)
            await driver.switch_to.window(handle)
            title = await driver.title
            if "BTG" in title:
                break
    except Exception as e:
        print(f"ERROR CHOOSE \n{e}")

    try:
        checkbox = await driver.find_element(By.XPATH, '//*[@id="fPay"]/div/label/label', timeout=20)
        await driver.execute_script("arguments[0].click();", checkbox)
    except Exception as e:
        print(f"ERROR CHECKBOX \n{e}")

    try:
        next_button = await driver.find_element(By.ID, 'btn_next', timeout=25)
        await driver.execute_script("arguments[0].click();", next_button)
    except Exception as e:
        print(f"ERROR NEXT BUTTON \n{e}")

    try:
        try:
            sleep(2.5)
            click_select = await driver.find_element(By.ID, 'TypeCurr_msdd', timeout=20)
            await click_select.click()
            sleep(3.5)
            choose_trc20 = await driver.find_element(By.XPATH, '//li[@class="enabled _msddli_ name15 GCZ"]', timeout=40)
            await choose_trc20.click()
        except Exception as e:
            print(f"ERROR CHOOSE TRC20")
        sleep(1)
        input_email = await driver.find_element(By.ID, 'email', timeout=10)
        await input_email.write(user_email)
        sleep(1)
        re_input_email = await driver.find_element(By.ID, 'Re_Enter_Email', timeout=10)
        await re_input_email.write(user_email)
        sleep(1)
        next_but = await driver.find_element(By.ID, 'pay_btn', timeout=10)
        await driver.execute_script("arguments[0].click();", next_but)
    except Exception as e:
        print(f"ERROR EMAIL \n{e}")


async def get_wallet():
    async with webdriver.Chrome(options=options) as driver:
        await login(driver)

        sleep(4.5)
        try:
            address_elem = await driver.find_element(By.XPATH, '(//div[@class="merchant-tabs__tab-address"])[4]/span', timeout=30)
            address = await address_elem.text

            amount_elem = await driver.find_element(By.XPATH, '//div[@class="sm_zag"]/span', timeout=30)
            amount = await amount_elem.text

        except Exception as e:
            print(f"ERROR DATA \n{e}")

        return {
            "address": address,
            "amount": amount.replace("USDT", '').replace(" ", ''),
            "currency": "usdt"
        }


def wallet():
    wallet_data = asyncio.run(get_wallet())
    print(wallet_data)
    return jsonify(wallet_data)
