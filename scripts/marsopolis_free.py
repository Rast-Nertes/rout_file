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

url = 'https://marsopolis.site/en/login'
user_email = "kiracase34@gmail.com"
user_password = "zE7iUEFYLweX7ta"

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


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.CSS_SELECTOR, 'main > div > div > form > label:nth-child(1) > input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.CSS_SELECTOR, 'main > div > div > form > label:nth-child(2) > input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'main > div > div > form > div.authincation__row.authincation__row--button > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        return {"status":"0", "ext":f"error login {e}"}

    sleep(3)
    driver.get('https://marsopolis.site/en/account/insert')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(50)
            choose_pay = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/form/div/div[2]/div[1]/div/label[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_pay)

            driver.implicitly_wait(30)
            input_amount = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/form/div/div[2]/div[2]/label/input')
            input_amount.clear()
            input_amount.send_keys('550')

            driver.implicitly_wait(30)
            replesh = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/form/div/div[2]/div[2]/div/button[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", replesh)
        except Exception as e:
            return {"status":"0", "ext":f"error replesh {e}"}

        sleep(3.5)
        windows = driver.window_handles
        for win in windows:
            driver.switch_to.window(win)
            print(driver.title)
            sleep(1.5)
            if not("sopo") in driver.title:
                break

        try:
            driver.implicitly_wait(60)
            choose_trc20 = driver.find_element(By.XPATH, '(//img[@alt="USDT (TRC20)"])[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            return {"status":"0", "ext":f"error choose trc20 {e}"}

        try:
            driver.implicitly_wait(60)
            submit_payment = driver.find_element(By.ID, 'submit-payment')
            sleep(1.5)
            submit_payment.click()
        except Exception as e:
            return {"status":"0", "ext":f"error submit {e}"}

        try:
            sleep(3.5)
            driver.implicitly_wait(60)
            address = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[7]/div[2]').text

            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[5]/div[1]/div[3]/div[5]/span').text

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