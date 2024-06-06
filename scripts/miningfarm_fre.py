from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://s1.mining-farms.lol/login'
user_email = "kiracase34@gmail.com"
user_password = "kiramira123"

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


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(50)
        input_email = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/form/div/table/tbody/tr[1]/td/input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(30)
        input_password = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/form/div/table/tbody/tr[2]/td/input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/form/div/table/tbody/tr[3]/td/input')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        return {"status":"0", "ext":f"error login {e}"}

    sleep(5.5)
    driver.get('https://s1.mining-farms.lol/account/insert')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(30)
            choose_frekassa = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[5]/div/div/b/div[3]/div[3]/a/img')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_frekassa)

            driver.implicitly_wait(40)
            input_amoun = driver.find_element(By.XPATH, '//*[@id="oa"]')
            input_amoun.clear()
            input_amoun.send_keys("650")

            driver.implicitly_wait(30)
            submit = driver.find_element(By.ID, 'submit')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit)
        except Exception as e:
            return {"status":"0", "ext":f"error choose freekassa {e}"}

        try:
            driver.implicitly_wait(30)
            next_step_button_2 = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[5]/div/div/div[2]/center/b/b/center/form/input[8]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step_button_2)
        except Exception as e:
            return {"status":"0", "ext":f"error next step button {e}"}

        try:
            driver.implicitly_wait(60)
            choose_trc20 = driver.find_element(By.ID, 'currency-15')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(40)
            input_email = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div/div[1]/div/form/div/div[2]/input')
            input_email.clear()
            input_email.send_keys(user_email)
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
