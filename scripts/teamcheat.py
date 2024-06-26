from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://teamcheat.ru/Pubg/Crooked'
user_email = "kiracase34@gmail.com"
user_password = "Kiramira000"

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
    actions = ActionChains(driver)

    try:
        driver.implicitly_wait(20)
        a_href = driver.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[1]/div[2]/div/div[1]/div/div/a').get_attribute('href')
        driver.get(a_href)
    except Exception as e:
        print(f'ERROR LINK \n{e}')

    try:
        driver.implicitly_wait(20)
        choose_click = driver.find_element(By.XPATH, '//*[@id="TypeCurr_msdd"]')
        sleep(1.5)
        choose_click.click()

        driver.implicitly_wait(20)
        choose_trc20 = driver.find_element(By.XPATH, '//span[@class="ddlabel" and text()="USDT"]')
        sleep(1.5)
        choose_trc20.click()
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    try:
        input_data(driver, 30, '//*[@id="email"]', user_email)
        input_data(driver, 30, '//*[@id="Re_Enter_Email"]', user_email)
        click(driver, 30, '//*[@id="pay_btn"]')
    except Exception as e:
        print(f'ERROR PLACE ORDER \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '//*[@id="form1"]/section/section/div[2]/div[2]/div[4]/div/div[1]/div/span').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '//*[@id="form1"]/section/section/div[2]/div[2]/div[4]/p/span').text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
