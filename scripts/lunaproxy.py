from seleniumwire import webdriver
from time import sleep
from flask import Flask, jsonify
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Paymentmars

#CONSTANS
user_login = 'kiracase34@gmail.com'
user_password = 'kiramira34'
url = 'https://www.lunaproxy.com/login/'

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False


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
        input_email = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="loginbox"]/div/div/div[3]/input'))
        )
        input_email.send_keys(user_login)

        input_password = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="loginbox"]/div/div/div[4]/input'))
        )
        input_password.send_keys(user_password)

        try:
            continue_log_in = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="loginbox"]/div/div/div[6]'))
            )
            continue_log_in.click()
            #Время, чтобы залогинился
            sleep(5)
        except Exception as e:
            print(f"LOG IN BUTTON ERROR \n{e}")

    except Exception as e:
        return {"status": "0", "ext": f"Login error. Check script. {e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        driver.get("https://www.lunaproxy.com/buy-proxy/")
        driver.execute_script("window.scrollBy(0, 100);")

        try:
            driver.implicitly_wait(10)
            click_accept = driver.find_element(By.XPATH, '//*[@id="allAcceptGoogleSetting"]')
            sleep(1)
            driver.execute_script("arguments[0].click();", click_accept)
        except:
            pass

        try:
            driver.implicitly_wait(20)
            choose_tariff = driver.find_element(By.XPATH, '//div[@class="inline_pay pay_btn " and @name="302"]')
            sleep(1.2)
            driver.execute_script("arguments[0].click();", choose_tariff)
        except Exception as e:
            try:
                driver.implicitly_wait(10)
                find_input_tag = driver.find_element(By.XPATH, '//*[@id="loginbox"]/div/div/div[3]/input')

                if find_input_tag:
                    return {"status": "0", "ext": "Login error. Check script."}

            except:
                return {"status": "0", "ext": f"error choose tariff {e}"}

        try:
            choose_crypto = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@class="li-content" and @data-box="12"]'))
            )
            sleep(1)
            driver.execute_script("arguments[0].click();", choose_crypto)
            sleep(2)

        except Exception as e:
            return {"status": "0", "ext": f"Choose crypto error {e}"}

        try:
            continue_to_pay = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//div[@class="primary-btn-mini handleToPay"]'))
            )
            continue_to_pay.click()
        except Exception as e:
            return {"status": "0", "ext": f"continue error  {e}"}

        try:
            sleep(7.5)
            new_window = driver.window_handles[1]
            driver.switch_to.window(new_window)

            trc_20 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[1]/div[2]/div/div[1]')
            driver.execute_script("arguments[0].click();", trc_20)

            driver.execute_script("window.scrollBy(0, 300);")

            amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[1]/div[3]/div[7]/div[2]/div[1]/p/i'))
            )
            amount = amount.text.replace("USDT", "")

            address = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[1]/div[3]/div[7]/div[1]/div[1]/p'))
            )
            address = address.text

            return {
                "address": address,
                "amount": amount.replace("$", ''),
                "currency": "usdt"
            }
        except Exception as e:
            return {"status": "0", "ext": f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)