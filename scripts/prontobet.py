from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://www.prontobet.com/en/login'
user_email = "kiracase34@gmail.com"
user_password = "EwyX7wsmp9@EGfB"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

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
        input_data(driver, 20, '//*[@id="username"]', user_email)
        input_data(driver, 20, '//*[@id="password"]', user_password)
        click(driver, 20, '/html/body/app-root/div/div/div[2]/app-main-overview/app-login-overview/section/div/div/app-login/form/div[3]/button')
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        click(driver, 20, '//a[text()=" Deposit "]')
    except Exception as e:
        find_input_tag = driver.find_element(By.XPATH, '//*[@id="username"]')
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"ERROR DEPOS BUT \n{e}")

    try:
        sleep(3.5)
        click(driver, 20, '//img[@alt="Crypto"]')
    except Exception as e:
        print(f'ERROR CHOOSE CRYPTO \n{e}')

    try:
        driver.implicitly_wait(30)
        select_tag = driver.find_element(By.CSS_SELECTOR, 'form > section > section.top-section > app-coins-paid > form > div.input-group > select')
        select = Select(select_tag)

        select.select_by_value('USDTT')
    except Exception as e:
        print(f'ERROR SELECT TRC20 \n{e}')

    try:
        click(driver, 20, '/html/body/app-root/div/ng-component/app-deposit-overview/div/app-deposit-step-one/form/footer/button')
    except Exception as e:
        print(f'ERROR DEPOS BUT \n{e}')

    try:
        driver.implicitly_wait(20)
        get_src = driver.find_element(By.ID, 'receiver').get_attribute('src')
        driver.get(get_src)
    except Exception as e:
        print(f'ERROR GET SRC \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '//*[@id="mui-10"]').get_attribute('value')

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '//*[@id="root"]/div/div/div[2]/div/div/div[2]/form[1]/div[1]/div/div/div/div/div/div/div/h2').text.replace("USDT", '').replace(" ", '')

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
