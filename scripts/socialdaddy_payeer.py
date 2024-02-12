#https://socialdaddy.net/login.aspx
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

app = Flask(__name__)
url = 'https://www.hostwinds.com'
user_login = 'kiracase34@gmail.com'
user_password = '341854985'

#CHROME CONSTANS

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False
chrome_options.add_argument('--disable-save-password-bubble')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

user_agent = UserAgent()
chrome_options.add_argument(f"user-agent={user_agent.random}")

#driver = webdriver.Chrome(options=chrome_options)

def login(driver):
    try:
        print("LOGIN START")
        driver.get('https://socialdaddy.net/login.aspx')
        driver.maximize_window()

        element_start__input_user_login = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_txtemail"]'))
        )
        element_start__input_user_login.send_keys(user_login)

        #Вводим пароль

        input_user_password = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_txtmobile"]'))
        )
        input_user_password.send_keys(user_password)

        #Заходим

        accept_registration = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_btnlogin"]'))
        )
        accept_registration.click()

        print("LOGIN ACCEPT")
    except Exception as e:
        print(f"LOGIN ERROR -- \n{e}")

def get_wallet_data():
    with webdriver.Chrome(options=chrome_options) as driver:
        login(driver)
        try:
            print("WALLET DATA START")
            driver.get('https://socialdaddy.net/balance.aspx')
            sleep(5)
            driver.refresh()
            sleep(3)
            #Add balance
            add_balance = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_btnsave"]'))
            )
            add_balance.click()
            #выбираем Payeer
            choose_pay = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="ContentPlaceHolder1_drppayment"]'))
            )
            choose_pay.click()
            sleep(3)
            choose_pay.send_keys(Keys.ARROW_DOWN)
            sleep(1)
            choose_pay.send_keys(Keys.ENTER)

            sleep(7)
            #Выбрали его
            input_amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/form/div[3]/div[1]/section[2]/div/div[1]/div/div/div[7]/div[1]/input'))
            )
            input_amount.send_keys('13')
            #Нажимаем кнопку
            accept_amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/form/div[3]/div[1]/section[2]/div/div[1]/div/div/div[7]/div[2]/input'))
            )
            accept_amount.click()

            #Выбираем ton
            choose_wallet = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div[3]/ul[1]/li[4]/div/div'))
            )
            choose_wallet.click()

            input_email =  WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="id_order_email"]'))
            )
            input_email.send_keys(user_login)

            #Подвтерждаем, введя почту
            accept_wallet = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/form/div[2]/div[4]/div[2]/a'))
            )
            accept_wallet.click()

            sleep(5)

            amount = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="info_bitcoin"]/div[1]/h3/font[1]'))
            )
            amount = amount.text.replace("USDT", "")

            address = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="info_bitcoin"]/div[1]/h3/font[2]'))
            )
            address = address.text
            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"WALLET DATA ERROR -- \n{e}")
            return None

@app.route('/api/selenium/socialdaddy_payeer')
def wallet():
    wallet_data = get_wallet_data()
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader = False, debug= True, port=5011)