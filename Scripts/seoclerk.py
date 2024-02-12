import cloudscraper
from selenium import webdriver
from time import sleep
from twocaptcha import TwoCaptcha
from flask import Flask, jsonify
from fake_useragent import UserAgent
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#NOWPAYMENTS

#CONSTANS
app = Flask(__name__)
scrap = cloudscraper.create_scraper()
user_login = 'kiramira123'
user_password = 'kiramira1'
url = 'https://www.seoclerk.com'

#API CONSTANS
api_key = '7f728c25edca4f4d0e14512d756d6868'

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

#driver = webdriver.Chrome(options= options)


def login(driver):

    driver.get(url)
    driver.maximize_window()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))

    iframe_element = driver.find_element(By.TAG_NAME, 'iframe')
    src = iframe_element.get_attribute('src')

    parsed_url = urlparse(src)
    query_params = parse_qs(parsed_url.query)
    recaptcha_key = query_params.get('k', [''])[0]

    print("Ключ reCAPTCHA:", recaptcha_key)

    solver = TwoCaptcha(api_key)

    result = solver.solve_captcha(site_key=recaptcha_key, page_url=url)
    print(f"РЕЗУЛЬТАТ: {str(result)}")

    try:
        try:
            block_delete = driver.find_element(By.XPATH, '/html/body/div[5]/div/div/div[2]/form/div[4]/div/div[1]/div/div')
            driver.execute_script('arguments[0].parentNode.removeChild(arguments[0]);', block_delete)
        except Exception as e:
            print("НЕ УДАЛОСЬ ИЗМЕНИТЬ")

        try:
            sleep(2)
            textarea_element = driver.find_element(By.XPATH, '//*[@id="g-recaptcha-response-1"]')
            driver.execute_script("arguments[0].removeAttribute('style');", textarea_element)
        except Exception as e:
            print(f"Block ERROR")

    except Exception as e:
        print("ERROR CAPTCHA")

    try:
        try:
            close_ = WebDriverWait(driver, 4).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="close"]'))
            )
            close_.click()
        except:
            pass

        sleep(1)
        button_to_login = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/header/div[2]/div/div/a[1]'))
        )
        button_to_login.click()
    except Exception as e:
        print(f"BUTTON ERROR \n{e}")

    try:
        login_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="l_username"]'))
        )
        login_input.send_keys(user_login)

        pass_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="l_password"]'))
        )
        pass_input.send_keys(user_password)

        textarea_element_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="g-recaptcha-response-1"]'))
        )
        textarea_element_input.send_keys(str(result))

        button_log_in = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="loginCheck"]/input[10]'))
        )
        sleep(1)
        button_log_in.click()
        sleep(1)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")


def get_wallet():
    try:
        with webdriver.Chrome(options=options) as driver:
            login(driver)
            driver.get('https://www.seoclerk.com/order/499921')
            try:
                check_button = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="stripeButton"]'))
                )
                check_button.click()

                driver.execute_script("window.scrollBy(0, 700);")
                sleep(1)
            except Exception as e:
                print(f"CHECKOUT ERROR \n{e}")

            try:
                choose_nowpayments = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="nowPayments-form-btn"]'))
                )
                choose_nowpayments.click()
            except Exception as e:
                print(f"NOW PAYMENTS ERROR \n{e}")

            try:
                choose_usdt_tron = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[1]/div[3]/div[1]/div'))
                )
                choose_usdt_tron.click()

                choose_usdt_tron_step_2 = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[1]/div[3]/div[1]/div[2]/div[2]/ul/li[2]'))
                )
                choose_usdt_tron_step_2.click()

                next_step = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[1]/div[3]/button'))
                )
                next_step.click()
            except Exception as e:
                print(f"CHOOSE TRON \n{e}")

            amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]'))
            )
            amount = amount.text.replace("USDT", "")

            address = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[1]'))
            )
            address = address.text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
    except Exception as e:
        print(f"GET WALLET ERROR \n{e}")
        return None

@app.route('/api/selenium/seoclerk')
def wallet():
    wallet_data = get_wallet()
    return jsonify(wallet_data)


if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5025)