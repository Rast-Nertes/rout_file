from time import sleep
from flask import Flask
from flask import jsonify
#from selenium import webdriver
from fake_useragent import UserAgent
from seleniumwire import webdriver
#import undetected_chromedriver2 as uc2
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#CONSTANS

url = 'https://arbitragescanner.io/'
user_login = 'kiracase34@gmail.com'
user_password = 'kiraoleg8'

#CHROME OPTIONS

options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("--disable-save-password-bubble")
options.add_argument('--disable-blink-features=AutomationControlled')
user_agent = UserAgent()
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0')
#driver = webdriver.Chrome(options=options)

def login(driver):
    try:
        print("LOGIN START")
        driver.get('https://www.lumiproxy.com/login/')
        driver.maximize_window()
        sleep(2)

        #Вводим логин
        element_start__input_user_login = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div/div[2]/div/div/div/form/div[1]/div/div[2]/input'))
        )
        element_start__input_user_login.send_keys(user_login)

        input_user_password = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div/div[2]/div/div/div/form/div[2]/div/div[2]/input')
        input_user_password.send_keys(user_password)

        accept_registration = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div/div[2]/div/div/div/form/div[3]/div/button'))
        )
        accept_registration.click()


        try:
            close = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div[3]/div/img'))
            )
            close.click()
        except:
            pass

        sleep(5)
        print("LOGIN SUCCEFUL")
    except Exception as e:
        print(f"LOGIN ERROR -- \n{e}")


def get_wallet_data():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        try:
            driver.get('https://www.lumiproxy.com/pricing/residential/')
            driver.execute_script("window.scrollBy(0, 1000);")
            start_now = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div[4]/div[1]/div[2]/div[2]/button'))
            )
            start_now.click()

            sleep(5)

            driver.execute_script("window.scrollBy(0, 250);")

            choose_currency= WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div[4]/div[3]/div/main[2]/header'))
            )
            choose_currency.click()

            accept_currency = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[2]/div[2]/div[4]/div[3]/div/footer/div[1]'))
            )
            accept_currency.click()

            sleep(5)
            new_window = driver.window_handles[1]
            driver.switch_to.window(new_window)

            sleep(12)
            #Trabl
            choose_usdt = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div/triplea-ecommerce-payment-v1/main/section/div/div/div/div/span/div/div[2]/div[2]/div/div[6]/div/div'))
            )
            choose_usdt.click()
            accept_usdt_20 = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="crypto-option-list"]/div/div[3]/div'))
            )
            accept_usdt_20.click()

            try:
                input_name = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="triplea-home"]/div/div/div/div/span/div/fieldset/div/input'))
                )
                input_name.send_keys("Rast")

                accept_name = WebDriverWait(driver, 1).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="terms-and-conditions"]'))
                )
                accept_name.click()
            except:
                pass

            sleep(6)
            amount = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="triplea-payment-form"]/div/div[3]/div[2]/div[1]/span[1]'))
            )
            amount = amount.text
            print(amount)

            address = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="triplea-payment-form"]/form/div[1]/div/div/div[1]'))
            )
            address = address.text
            print(address)
            return {
                "address":address,
                "amount":amount,
                "currency":"usdt"
            }

        except Exception as e:
            print(f"WALLET DATA ERROR \n{e}")
            return None


def wallet():
    wallet_data = get_wallet_data()
    print(wallet_data)
    return jsonify(wallet_data)