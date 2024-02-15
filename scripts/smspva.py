import cloudscraper
import requests
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

#

#CONSTANS
app = Flask(__name__)
scrap = cloudscraper.create_scraper()
user_login = 'kiracase34@gmail.com'
user_password = 'kirapva122'
url = 'https://smspva.com/signin.html'

#API CONSTANS
api_key = '7f728c25edca4f4d0e14512d756d6868'

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

#driver = webdriver.Chrome(options= options)
#driver.get('https://smspva.com/signin.html')
#driver.maximize_window()
def cloud_captcha_and_login(driver):
    driver.get('https://smspva.com/signin.html')
    driver.maximize_window()

    try:
        input_email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="login"]'))
        )
        input_email.send_keys(user_login)

        input_password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]'))
        )
        input_password.send_keys(user_password)

    except Exception as e:
        print(f"ERROR INPUT \n{e}")

    find_site_key = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="dle-content"]/div/div[3]/ul/li[4]/div/div'))
    )
    site_key = find_site_key.get_attribute('data-sitekey')
    print(site_key)
    api = api_key

    try:
        delete_type = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'cf-turnstile-response'))
        )
        delete_type_script = """
        var element = document.querySelector('input[name="cf-turnstile-response"]');
        element.removeAttribute('type');
        """
        driver.execute_script(delete_type_script)
    except Exception as e:
        print(f"ERROR DELETE \n{e}")

    response = requests.get(
        f'http://2captcha.com/in.php?key={api_key}&method=turnstile&sitekey={site_key}&pageurl={url}')
    request_status, captcha_id = response.text.split('|')

    if request_status == 'OK':
        while True:
            # Проверяем, решена ли капча
            captcha_response = requests.get(f'http://2captcha.com/res.php?key={api_key}&action=get&id={captcha_id}')

            if captcha_response.text.startswith('OK'):
                captcha_solution = captcha_response.text.split('|')[1]
                print(f'CAPTCHA успешно решена. Решение: {captcha_solution}')
                break  # Выходим из цикла, так как капча решена
            elif captcha_response.text == 'CAPCHA_NOT_READY':
                print("Капча еще в процессе решения!")
                sleep(5)
            else:
                print(f'Ошибка при получении ответа от 2Captcha: {captcha_response.text}')
                break  # Выходим из цикла в случае ошибки

    try:
        insert_text_script = f"""
        var element = document.querySelector('input[name="cf-turnstile-response"]');
        element.value = '{captcha_solution}';
        """
        driver.execute_script(insert_text_script)
    except Exception as e:
        print(f'ERROR INPUT TOKEN')

    try:
        sig_in = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="dle-content"]/div/div[3]/div[1]/button'))
        )
        sig_in.click()
    except Exception as e:
        print(f'ERROR BUTTON \n{e}')
    #Даем время авторизоваться
    sleep(5)


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        cloud_captcha_and_login(driver)
        driver.get('https://smspva.com/pay-systems.html')
        try:
            choose_cryptocurrency = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="payment_systems"]/div[2]/div[1]/div[1]/div[2]/div/div/button'))
            )
            choose_cryptocurrency.click()
        except Exception as e:
            print(f'CHOOSE CRYPTOCURRENCY ERROR \n{e}')

        try:

            close_adv = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]/div[2]/form/div[3]/button[2]'))
            )
            close_adv.click()
        except Exception as e:
            pass

        try:
            choose_usdt_trc20 = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="payment_systems"]/div[2]/div/form/div/div[2]/div/label[3]/div'))
            )
            choose_usdt_trc20.click()

            sleep(2)
            driver.execute_script("window.scrollBy(0, 500);")
        except Exception as e:
            print(f"ERROR CHOOSE USDT TRC20 \n{e}")

        try:
            pay_now = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="payment_systems"]/div[2]/div/form/button'))
            )
            pay_now.click()
        except Exception as e:
            print(f'BUTTON PAY NOW ERROR \n{e}')

        amount = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="__next"]/main/section/div/div[1]/div[1]/div[1]/div[2]/div[2]/p'))
        )
        amount = amount.text

        address = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="__next"]/main/section/div/div[1]/div[1]/div[1]/div[3]/div[2]/p'))
        )
        address = address.text

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }

def wallet():
    wallet_data = get_wallet()
    return jsonify(wallet_data)
