from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

#CONSTANS

url = 'https://mirsliva.com/login'
user_login = "kiracase34"
user_password = "zWcBvXGiA2FkD4n"

def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[2]/div/div/form/div[1]/div/dl[1]/dd/input')
        input_email.clear()
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/div/div[2]/div[2]/div/div/form/div[1]/div/dl[2]/dd/div/div/input')
        input_password.clear()
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        click_to_login = driver.find_element(By.CSS_SELECTOR, 'div.p-body-content > div > div > form > div.block-container > dl > dd > div > div.formSubmitRow-controls > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", click_to_login)
        sleep(5)
    except Exception as e:
        print(f"BUTTON ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        driver.get("https://mirsliva.com/account/upgrades")

        try:
            driver.implicitly_wait(10)
            button_buy = driver.find_element(By.CSS_SELECTOR, 'div.block.block-upgrade.block-upgrade--2 > div > div.block-body.block-body--main > div.block-row.block-row--pay > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", button_buy)
        except Exception as e:
            print(f"BUTTON BUY ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_payment = driver.find_element(By.CSS_SELECTOR, 'div.block.block-upgrade.block-upgrade--2.providerSelect-active > div > div.block-body.block-body--providerSelect > div:nth-child(1) > a > span')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_payment)
        except Exception as e:
            print(f"CHOOSE PAYMENT ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_currency = driver.find_element(By.CSS_SELECTOR, 'div > div.payment1__method > div.payment1__list > label:nth-child(3) > span')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_currency)
        except Exception as e:
            print(f"CHOOSE CURRENCY ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            buy_button = driver.find_element(By.CSS_SELECTOR, 'body > div > section > div > div.payment1__method > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_button)
        except Exception as e:
            print(f"BUY BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(30)
            buy_with_trc_20 = driver.find_element(By.CSS_SELECTOR, 'div.total.col-span-12.md\:col-span-6.lg\:col-span-4.hidden.md\:block.dark\:bg-dark-layout > div.total__footer.border-dot.dark\:bg-dark-layout > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_with_trc_20)

            sleep(5)

            driver.implicitly_wait(10)
            buy_with_trc = driver.find_element(By.CSS_SELECTOR, 'div.total.col-span-12.md\:col-span-6.lg\:col-span-4.hidden.md\:block.dark\:bg-dark-layout > div.total__footer.border-dot.dark\:bg-dark-layout > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_with_trc)
        except Exception as e:
            print(f"BUY WITH TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(30)
            address = driver.find_element(By.CSS_SELECTOR,
                                          'div.col-span-9.ms-16 > div > div.data-info.pt-12 > div.data-info__address.flex.items-center.justify-between > div > span').text
            driver.implicitly_wait(30)
            amount = driver.find_element(By.CSS_SELECTOR,
                                         'div.total.col-span-12.md\:col-span-6.lg\:col-span-4.hidden.md\:block.dark\:bg-dark-layout > div.total__footer.border-dot.dark\:bg-dark-layout > div:nth-child(1) > span:nth-child(2)').text.replace("USDT", "").replace(" ", "")
            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }

        except Exception as e:
            print(f"DATA ERROR \n{e}")
            return None

def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
