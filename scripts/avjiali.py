from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://join.avjiali.com/signup/signup.php?'
user_email = "yewoxo4550@otemdi.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
# options.add_argument('--headless')

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1)
    driver.execute_script("arguments[0].click();", elem_click)
    sleep(1)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        input_data(driver, 35, '//*[@id="email"]', user_email)
    except Exception as e:
        print(f'ERROR INPUT EMAIL \n{e}')

    try:
        click(driver, 35, '//*[@id="form"]/label[3]')
        sleep(1)
        click(driver, 20, '//*[@id="join_normal_crypto"]/label[1]')
    except Exception as e:
        print(f'ERROR CHOOSE CRYPTO \n{e}')

    try:
        click(driver, 20, '//*[@id="form"]/input[22]')
    except Exception as e:
        print(f'ERROR SUBMIT BUTTON \n{e}')

    try:
        input_data(driver, 45, '//*[@id="first_name"]', "Kira")
        sleep(1)
        input_data(driver, 20, '//*[@id="last_name"]', 'Ivanova')
    except Exception as e:
        print(f"ERROR INPUT DATA \n{e}")

    try:
        click(driver, 20, '//*[@id="btn_USDT.TRC20"]')
    except Exception as e:
        print(f"ERROR CHOOSE TRC20 \n{e}")

    try:
        click(driver, 20, '//*[@id="btnCheckout"]')
    except Exception as e:
        print(f"ERROR SUBMIT \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            sleep(6.5)
            address = WebDriverWait(driver, 35).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="email-form"]/div[2]/div[1]/div[3]/div[2]'))
            )
            address = address.text

            amount = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="email-form"]/div[2]/div[1]/div[1]/div[2]'))
            )
            amount = amount.text.replace('USDT.TRC20', '').replace(" ", '')

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
