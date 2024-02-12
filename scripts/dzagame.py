from time import sleep
from flask import Flask
from flask import jsonify
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#CONSTANS

app = Flask(__name__)
url = 'https://www.dzagame.com/en/my-account/'
user_login = 'kiracase34@gmail.com'
user_password = 'oleg321123!'

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
        driver.get('https://www.dzagame.com/en/my-account/')
        driver.maximize_window()

        element_start__input_user_login = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="username"]'))
        )
        element_start__input_user_login.send_keys(user_login)

        #Вводим пароль

        input_user_password = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]'))
        )
        input_user_password.send_keys(user_password)

        #Заходим

        accept_registration = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="customer_login"]/div[1]/form/p[4]/button'))
        )
        accept_registration.click()

        print("LOGIN ACCEPT")
    except Exception as e:
        print(f"LOGIN ERROR -- \n{e}")

def get_wallet_data():
    try:
        with webdriver.Chrome(options=chrome_options) as driver:
            login(driver)
            driver.get('https://www.dzagame.com/en/shop/')

            driver.execute_script("window.scrollTo(0, 200);")

            get_in_shop = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div[3]/div/ul/li[7]/div/div[2]/div/div/a'))
            )
            get_in_shop.click()

            plus_item = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/article/div/div/div[3]/div/form/table/tbody/tr[1]/td[5]/div/button[2]'))
            )
            sleep(2)
            for _ in range(5):
                plus_item.click()
                sleep(1)

            accept_items_in_busket = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/article/div/div/div[3]/div/form/table/tbody/tr[2]/td/div/button'))
            )
            accept_items_in_busket.click()

            driver.execute_script("window.scrollTo(0, 500);")

            proceed_to_checkout = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/article/div/div/div[3]/div/div/div/div/a'))
            )
            proceed_to_checkout.click()

            sleep(4)

            accept_wallet = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div/div/div[1]/div/article/div/div/form/div/div[2]/div/div/div/div/div/div[3]/div/p/label/input')
            driver.execute_script("arguments[0].click();", accept_wallet)

            driver.execute_script("window.scrollTo(0, 1800);")

            place_order = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="place_order"]'))
            )
            place_order.click()

            pay_ = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/article/div/div/form/input[7]'))
            )
            pay_.click()

            choose_usdt = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div[3]/ul[1]/li[2]/div'))
            )
            choose_usdt.click()

            input_accept_usdt = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="id_order_email"]'))
            )
            input_accept_usdt.send_keys(user_login)

            accept_usdt = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/form/div[2]/div[4]/div[2]/a'))
            )
            accept_usdt.click()


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

@app.route('/api/selenium/dzgame')
def wallet():
    wallet_data = get_wallet_data()
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5014)