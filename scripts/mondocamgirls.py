from time import sleep
from flask import jsonify
from seleniumwire.thirdparty.mitmproxy.net.tls import VERSION_CHOICES
from seleniumwire import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://alice-hall.mondocamgirls.com/en'
user_email = "yewoxo4550@otemdi.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

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
    sleep(1.5)
    driver.execute_script("arguments[0].click();", elem_click)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        click(driver, 10, '//*[@id="disclaimer-cadre"]/a[1]')
    except:
        pass

    try:
        click(driver, 30, '//*[@id="tabella_prezzi"]/tbody/tr[2]/td[1]/a')
    except Exception as e:
        print(f'ERROR BUY BUTT \n{e}')

    try:
        input_data(driver, 20, '//*[@id="multi_email"]', user_email)
        sleep(1)
        click(driver, 20, '//*[@id="pagpag_bitcoin"]')
    except Exception as e:
        print(f"ERROR INPUT EMAIL\n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            click(driver, 60, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div/label[10]/span[2]/div')
            sleep(1)
            click(driver, 20, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/button')
        except Exception as e:
            print(f'ERROR CHOOSE USDT \n{e}')

        try:
            input_data(driver, 35, '//*[@id="__next"]/div/div/div[2]/div[1]/form/div/div[2]/input', user_email)
            sleep(1)
            click(driver, 20, '//*[@id="__next"]/div/div/div[2]/div[1]/div[2]/button')
        except Exception as e:
            print(f'ERROR INPUT EMAIL \n{e}')

        try:
            click(driver, 40, '//*[@id="__next"]/div/div/div[2]/div[3]/div/div/label[3]')
            sleep(1)
            click(driver, 20, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div[2]/div/button')
        except Exception as e:
            print(f'ERROR CHOOSE NET \n{e}')

        try:
            driver.set_window_size(1000, 500)
            sleep(5.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[6]/div/div[2]/div/p').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/p').text.replace("USDT", '').replace(" ", '')

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
