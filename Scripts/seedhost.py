import cloudscraper
from selenium import webdriver
from time import sleep
from urllib.parse import urlparse, parse_qs
from twocaptcha import TwoCaptcha
from flask import Flask, jsonify
from fake_useragent import UserAgent
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#Coingate


#CONSTANS
app = Flask(__name__)
scrap = cloudscraper.create_scraper()
user_login = 'kiracase34@gmail.com'
user_password = 'kiramira11'
url = 'https://www.seedhost.eu/whmcs/clientarea.php'

#API CONSTANS
api_key = '7f728c25edca4f4d0e14512d756d6868'

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

def login(driver):

    driver.get(url)
    driver.maximize_window()

    try:
        input_email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="username"]'))
        )
        input_email.send_keys(user_login)

        input_password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]'))
        )
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        sleep(2)
        textarea_element = driver.find_element(By.XPATH, '//*[@id="g-recaptcha-response"]')
        driver.execute_script("arguments[0].style.display = 'block';", textarea_element)

        # Изменяем свойство margin
        driver.execute_script("arguments[0].style.margin = '100px 25px';", textarea_element)
    except Exception as e:
        print(f"TEXTAREA ERROR \n{e}")

    try:
        iframe_element = driver.find_element(By.TAG_NAME, 'iframe')
        src = iframe_element.get_attribute('src')
        #print(src)
        parsed_url = urlparse(src)
        query_params = parse_qs(parsed_url.query)
        recaptcha_key = query_params.get('k', [''])[0]

        print("Ключ reCAPTCHA:", recaptcha_key)

        solver = TwoCaptcha(api_key)
        key = solver.recaptcha(sitekey=recaptcha_key, url=url)
        result = key["code"]
        print(f"RESULT RECAPTCHA: {result}")
    except Exception as e:
        print(f"FIND KEY ERROR \n{e}")

    try:
        input_captcha_result = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="g-recaptcha-response"]'))
        )
        input_captcha_result.send_keys(result)

        try:
            log_in = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/div[4]/div[2]/form/div/fieldset/div[3]/div[1]/input'))
            )
            log_in.click()
        except Exception as e:
            print(f'BUTTON ERROR \n{e}')

    except Exception as e:
        print(f"LOG IN ERROR \n{e}")

def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        actions = ActionChains(driver)
        driver.get('https://www.seedhost.eu/whmcs/clientarea.php?action=addfunds')

        try:
            choose_wallet = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="paymentmethod"]'))
            )
            choose_wallet.click()
            for _ in range(3):
                actions.send_keys(Keys.ARROW_DOWN).perform()
                sleep(0.5)

            actions.send_keys(Keys.ENTER).perform()

            try:
                add_funds_button = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="wrapper"]/div[4]/div[2]/form/div/p/input'))
                )
                add_funds_button.click()
            except Exception as e:
                print(f"ADD FUNDS \n{e}")

        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")

        try:
            input_currency = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[3]/input'))
            )
            input_currency.send_keys("Us")

            choose_tether = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div/label[1]'))
            )
            choose_tether.click()

            button_continue = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[5]/div/div[2]/div/button'))
            )
            button_continue.click()

            continue_without_email = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[1]/div[2]/button[2]'))
            )
            continue_without_email.click()
        except Exception as e:
            print(f"Choose tether error \n{e}")

        try:
            choose_trc20_network = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[3]/div/div/label[4]'))
            )
            driver.execute_script("arguments[0].click();", choose_trc20_network)

            continue_choose = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[4]/div/div[2]/div/button'))
            )
            continue_choose.click()
        except Exception as e:
            print(f"CHOOSE TRC20 ERROR \n{e}")

        try:
            sleep(1)
            driver.set_window_size(1000, 750)
            sleep(1)
            amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '/html/body/div/div/div/div[2]/div[5]/div/div[2]/div/p'))
            )
            amount = amount.text.replace("USDT", "")

            address = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="__next"]/div/div/div[2]/div[6]/div/div[2]/div/p'))
            )
            address = address.text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")

@app.route("/api/selenium/seedhost")
def wallet():
    wallet_data = get_wallet()
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5030)
