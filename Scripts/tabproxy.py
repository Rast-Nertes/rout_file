import requests
from time import sleep
from flask import Flask
from flask import jsonify
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#CONSTANS

app = Flask(__name__)
url = 'https://www.tabproxy.com/login'
user_login = 'kiracase34@gmail.com'
user_password = 'proxycase1'

#API CONSTANS

API_KEY = '7f728c25edca4f4d0e14512d756d6868'
API_URL = 'http://rucaptcha.com/in.php'
API_RESULT_URL = f'http://rucaptcha.com/res.php?key={API_KEY}&action=get'


#CHROME CONSTANS

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False
chrome_options.add_argument('--disable-save-password-bubble')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

user_agent = UserAgent()
chrome_options.add_argument(f"user-agent={user_agent.random}")

def get_wallet_data():
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get('https://www.tabproxy.com')
        driver.maximize_window()

        pricing = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="header"]/div[1]/div[2]/div[1]'))
        )
        pricing.click()

        start_trial = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="pay_box"]/div/div[1]/div[1]/div'))
        )
        start_trial.click()

        input_email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="order_form_flow"]/div/div/div[6]/input[1]'))
        )
        input_email.send_keys(user_login)

        input_password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="order_form_flow"]/div/div/div[6]/input[2]'))
        )
        input_password.send_keys(user_password)


        driver.execute_script("window.scrollBy(0, 200);")

        buy_proxy = WebDriverWait(driver,10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="order_form_flow"]/div/div/div[6]/div[4]'))
        )
        buy_proxy.click()

        sleep(10)
        new_window = driver.window_handles[1]
        driver.switch_to.window(new_window)

        trc_20 = driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[1]/div[2]/div/div[1]')
        driver.execute_script("arguments[0].click();", trc_20)
        # trc_20 = WebDriverWait(driver, 10).until(
        #     EC.visibility_of_element_located((By.CSS_SELECTOR, "div.total-li[data-index='0'] > div.d-flex.align-items-center"))
        # )
        # trc_20.click()

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
            "amount": amount,
            "currency": "usdt"
        }

    except Exception as e:
        print(f"GET WALLET ERROR -- \n{e}")
        return None

@app.route('/api/selenium/tabproxy')
def wallet():
    wallet_data = get_wallet_data()
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5015)
