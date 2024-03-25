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

url = 'https://www.xvideos.red'
user_email = "kiracase34@gmail.com"
user_password = ")HgqVE@f#D3ZZ@@"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
# options.add_argument('--headless')

proxy_address = "62.3.13.13"
proxy_login = '1QjtPL'
proxy_password = 'pHSyxy'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_address}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        login_button = driver.find_element(By.ID, 'main-signin-btn')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"ERROR LOGIN BUTTON \n{e}")

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.ID, 'signin-form_login')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.ID, 'signin-form_password')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '//*[@id="signin-form"]/div[6]/div/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)

        sleep(5)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            driver.implicitly_wait(20)
            accept = driver.find_element(By.CSS_SELECTOR, 'div > button.btn.btn-primary.disclaimer-enter-straight')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", accept)
        except:
            pass

        try:
            driver.implicitly_wait(50)
            choose_crypto = driver.find_element(By.XPATH, '//div[@data-x-value="USDT"]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_crypto)
        except Exception as e:
            print(f"ERROR CHOOSE USDT \n{e}")

        try:
            driver.implicitly_wait(30)
            buy_now_button = driver.find_element(By.CSS_SELECTOR, 'div > button > span.submit-txt-product.submit-txt-product-697')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_now_button)
        except Exception as e:
            print(f"ERROR BUY NOW BUTTON \n{e}")

        try:
            driver.implicitly_wait(40)
            choose_network = driver.find_element(By.CSS_SELECTOR, 'div.invoice__steps > div.choose-currency-step > div.currencies-select > div')
            sleep(1.5)
            choose_network.click()
        except Exception as e:
            print(f"Reload Script...")
            driver.close()
            driver.quit()
            return wallet()

        try:
            driver.implicitly_wait(10)
            choose_tron = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[1]/div[3]/div[1]/div[2]/div[2]/ul/li[2]')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_tron)
        except Exception as e:
            print(f"ERROR CHOOSE TRX \n{e}")

        try:
            while True:
                try:
                    driver.implicitly_wait(40)
                    next_step_button = driver.find_element(By.CSS_SELECTOR, 'div.invoice__steps > div.choose-currency-step > button')
                    sleep(2)
                    driver.execute_script("arguments[0].click();", next_step_button)
                    sleep(1)
                except:
                    break
        except Exception as e:
            print(f"ERROR NEXT STEP \n{e}")

        try:
            driver.implicitly_wait(60)
            address = driver.find_element(By.CSS_SELECTOR, 'div.send-deposit-step > div.send-deposit-step__body > div.send-deposit-step__info > div:nth-child(2) > div.payment-info-item__content > div > div.copy-text__box').text

            driver.implicitly_wait(10)
            amount = driver.find_element(By.CSS_SELECTOR, 'div.send-deposit-step > div.send-deposit-step__body > div.send-deposit-step__info > div:nth-child(1) > div.payment-info-item__content > div > div.copy-text__box').text.replace('USDT', '').replace(' ', '').replace("TRX", '').replace("\n", '')

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
