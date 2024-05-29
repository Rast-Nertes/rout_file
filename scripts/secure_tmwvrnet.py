from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://secure.tmwvrnet.com/signup/signup.php?step=signup&nats=MzAxMjI1LjUuNDQuNDQuMC4wLjAuMC4w&switched=1&strack=0&'
user_email = "nadijev218@qiradio.com"
user_password = "Qwerty17"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
options.add_argument("--disable-save-password-bubble")
options.add_argument('--log-level=3')
options.add_argument('--disable-remote-fonts')
options.add_experimental_option('prefs', {'intl.accept_languages': 'en, en_US'})

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def wait_visibility(driver, time, XPATH):
    WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.XPATH, XPATH))
    )
    sleep(2.5)


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    elem_click.click()


def js_click(driver, time, XPATH):
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
    actions = ActionChains(driver)
    driver.maximize_window()
    driver.get(url)

    try:
        wait_visibility(driver, 50, '//*[@id="email"]')
        input_data(driver, 10, '//*[@id="email"]', user_email)
        input_data(driver, 10, '//*[@id="password"]', user_password)
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    try:
        click(driver, 10, '/html/body/div[1]/main/div[3]/div[2]')
        click(driver, 10, '//*[@id="crypto-cascade"]')
        click(driver, 10, '//*[@id="submit-button"]')
    except Exception as e:
        print(f'error accept payment \n{e}')

    try:
        wait_visibility(driver, 30, '//div[@class="pmLogo pmLogo_crypto pmChangeLogo_crypto  "]')
        click(driver, 10, '//div[@class="pmLogo pmLogo_crypto pmChangeLogo_crypto  "]')
    except Exception as e:
        print(f'ERROR CHOOSE crypto payment \n{e}')

    try:
        wait_visibility(driver, 30, '//div[@data-icon="USDT_TRX"]')
        click(driver, 10, '//div[@data-icon="USDT_TRX"]')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div[1]')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//div[@class="inner-price"]')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace("(5 USD)", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
