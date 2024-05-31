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

url = 'https://bmb-original.org/ru/login'
user_email = "kiracase34@gmail.com"
user_password = "mpTnWcAcZhmAhP8"

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@45.130.254.133:8000",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div[2]/div/div/div/form/label[1]/input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(15)
        input_password = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div[2]/div/div/div/form/label[2]/input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div[2]/div/div/div/form/div[2]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        return {"status":"0", "ext":f"error login {e}"}

    try:
        driver.implicitly_wait(30)
        insert_button = driver.find_element(By.XPATH, '/html/body/div[1]/aside/div/nav/ul[2]/li[5]/a')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", insert_button)
    except Exception as e:
        return {"status":"0", "ext":f"error insert button {e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(30)
            input_amount = driver.find_element(By.XPATH, '//*[@id="payblock"]/label/input')
            input_amount.clear()
            input_amount.send_keys('550')

            driver.implicitly_wait(20)
            choose_freekassa = driver.find_element(By.XPATH, '/html/body/div[1]/main/div/div/div/div/div[4]/div[2]/div/form[1]/button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_freekassa)
        except Exception as e:
            return {"status":"0", "ext":f"error choose {e}"}

        try:
            sleep(5.5)
            driver.switch_to.window(driver.window_handles[1])
            driver.refresh()
            sleep(2)
        except Exception as e:
            return {"status":"0", "ext":f"error switch {e}"}

        try:
            driver.implicitly_wait(60)
            choose_trc20 = driver.find_element(By.ID, 'currency-15')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            return {"status":"0", "ext":f"error input email {e}"}

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
