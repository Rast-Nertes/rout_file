from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://noveltydocumentstore.ws/product/uk-driving-license-psd-template-in-background-effect-photo-card-new-update-v3/index.php'
user_login = "kiracase34@gmail.com"
user_password = "kiramira555"

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
#options.add_argument("--headless")
options.headless = False

def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        driver.get(url)
        driver.maximize_window()
        sleep(5)
        try:
            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '//*[@id="product-1104"]/div[1]/div[2]/p[1]/span/ins/span/bdi').text.replace("$", "")

            driver.implicitly_wait(20)
            address = driver.find_element(By.XPATH, '/html/body/div[2]/main/div[2]/article/div[2]/div[2]/article/div[1]/div[2]/table/tbody[1]/tr[4]/td[2]').text

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
