from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://96.com/en/#/'
user_email = "kiracase34"
user_password = "vYN94@RKgd23"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
options.add_argument(f"user-agent={user_agent}")
options.add_argument("--disable-save-password-bubble")
options.add_argument('--log-level=3')
options.add_argument('--disable-remote-fonts')
options.add_argument("--auto-open-devtools-for-tabs")
options.add_experimental_option('prefs', {'intl.accept_languages': 'en, en_US'})

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

# proxy_address = "196.19.121.187"
# proxy_login = 'WyS1nY'
# proxy_password = '8suHN9'
# proxy_port = 8000


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
        js_click(driver, 30, '/html/body/div[1]/div[1]/div[1]/header/div/div/div[2]/div[1]/span')
        input_data(driver, 30, '/html/body/div[1]/div[2]/div/div/div/div[4]/div/input', user_email)
        input_data(driver, 30, '//*[@id="app"]/div[2]/div/div/div/div[5]/div/input', user_password)
        click(driver, 30, '//*[@id="app"]/div[2]/div/div/div/button/span')
    except Exception as e:
        return {"status":"0", "ext":f"error login \n{e}"}

    sleep(3.5)
    driver.get('https://96.com/en/page_recharge/#/')

    try:
        input_data(driver, 30, '//*[@id="component-2"]', '10')
        sleep(4.5)
        js_click(driver, 30, '//*[@id="animbtn"]/div')
    except Exception as e:
        return {"status":"0", "ext":f"error depos \n{e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//*[@id="app"]/section/main/div[1]/div/div/div[3]/dl/dd[1]/span/span[1]')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="app"]/section/main/div[1]/div/div/div[3]/dl/dd[3]')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
