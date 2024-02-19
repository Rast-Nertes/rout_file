import requests
from seleniumwire import webdriver
from time import sleep
from urllib.parse import urlparse, parse_qs
from anticaptchaofficial.imagecaptcha import *
from flask import Flask, jsonify
from fake_useragent import UserAgent
from urllib.parse import urlparse, parse_qs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

#Whitebit
#https://cryptofiat.finance/exchange-visamatertry-to-usdttrc20/

#CONSTANS
app = Flask(__name__)
user_login = 'kiracase34'
user_password = 'S8u6BjV6BmPnun5'
url = 'https://cryptofiat.finance'

#API CONSTANS

API_KEY = '7f728c25edca4f4d0e14512d756d6868'
API_URL = 'http://rucaptcha.com/in.php'
API_RESULT_URL = f'http://rucaptcha.com/res.php?key={API_KEY}&action=get'

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.add_experimental_option("detach", True)

#PROXY_CONSTANS

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@45.130.254.133:8000",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


#driver = webdriver.Chrome(options= options)

def login(driver):
    driver.get(url)
    driver.maximize_window()
    try:
        button_for_login = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div/div[3]/div[2]/div/div/div[1]/div[3]/span[1]'))
        )
        button_for_login.click()

    except Exception as e:
        print(f"BUTTON ERROR \n{e}")

    try:
        input_email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'form_field_id-5-logmail'))
        )
        input_email.send_keys(user_login)

        input_pass = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'form_field_id-5-pass'))
        )
        input_pass.send_keys(user_password)

    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        log_in_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="container"]/div/div[1]/div/div[2]/div/div[1]/form/button'))
        )
        log_in_button.click()
    except Exception as e:
        print(f"LOG IN BUTTON \n{e}")

def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)
        sleep(1)
        driver.get('https://cryptofiat.finance/exchange-usdttrc20-to-advcusd/')

        driver.implicitly_wait(10)
        element_to_remove = driver.find_element(By.CSS_SELECTOR, ".tophead_ins")
        driver.execute_script("arguments[0].remove();", element_to_remove)

        driver.implicitly_wait(10)
        element_to_remove_2 = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]')
        driver.execute_script("arguments[0].remove();", element_to_remove_2)

        driver.implicitly_wait(10)
        сaptcha_text = driver.find_element(By.XPATH, '//*[@id="exch_html"]/div[2]/div/div[3]/div[1]')
        driver.execute_script("arguments[0].innerText = 'THIS IS MATH EXAMPLE!!!';", сaptcha_text)

        try:
            value = driver.find_element(By.XPATH, '//*[@id="exch_html"]/div[2]/div/div[1]/div[1]/div[2]/div/div[4]/div[2]/input')
            driver.execute_script("arguments[0].value = '11';", value)

            #После ввода ссумы обновляется страница
            print("Ввел")
            sleep(1)

            tg_account = driver.find_element(By.XPATH, '//*[@id="cf8"]')
            driver.execute_script("arguments[0].value = '@sobaka'", tg_account)

            account_payeer = driver.find_element(By.XPATH, '//*[@id="account2"]')
            driver.execute_script("arguments[0].value = 'U';", account_payeer)

            try:
                ticket = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[4]/div[1]/div[1]/form/div/div[2]/div[2]/div/div[5]/input')
                driver.execute_script("arguments[0].click();", ticket)
            except Exception as e:
                print(f"TICKET ERROR \n{e}")
                return None

            driver.set_window_size(200, 300)
            driver.execute_script("window.scrollBy(0, 1300);")
            sleep(1)
            driver.save_screenshot("captcha.jpeg")
            sleep(2)
            driver.maximize_window()

            try:
                solver = imagecaptcha()
                solver.set_verbose(1)
                solver.set_key("6ab87383c97cb688c42b47e81c96bbcc")

                captcha_text = solver.solve_and_return_solution("captcha.jpeg")

                if captcha_text != 0:
                    print("captcha text " + captcha_text)
                else:
                    print("task finished with error " + solver.error_code)
            except Exception as e:
                print(f"CAPTCHA ERROR \n{e}")

            # try:
            #     # Загружаем капчу
            #     with open('captcha.png', 'rb') as captcha_file:
            #         data = {
            #             'key': API_KEY,
            #             'method': 'post'
            #         }
            #         response = requests.post(API_URL, data=data, files={'file': captcha_file})
            #     # Проверяем успешное выполнение капчи
            #     response_text = response.text.split('|')
            #     if response_text[0] == "OK":
            #         captcha_id = response_text[1]
            #         print(f"Капча успешно отправлена. ID капчи: {captcha_id}")
            #
            #         # Повторяем запросы для получения результата
            #         while True:
            #             result_response = requests.get(f"{API_RESULT_URL}&id={captcha_id}")
            #             if 'OK' in result_response.text:
            #                 captcha_solution = result_response.text.split('|')[1]
            #                 print(f"Captcha решена: {captcha_solution}")
            #                 break
            #
            #             elif 'CAPCHA_NOT_READY' in result_response.text:
            #                 print("Ожидание решения капчи...")
            #                 sleep(5)  # Подождите некоторое время перед повторным запросом
            #             else:
            #                 print("Ошибка при получении результата.")
            #                 print(result_response.text)
            #                 break
            # except Exception as e:
            #     print(f"CAPTHCA ERROR \n{e}")
            #     return None

            try:
                input_captcha = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="exch_html"]/div[2]/div/div[3]/div[2]/input'))
                )
                input_captcha.clear()
                input_captcha.send_keys(captcha_text)
            except Exception as e:
                print(f"INPUT CAPCTHA \n{e}")
                return None

            button = driver.find_element(By.XPATH, '//*[@id="exch_html"]/div[2]/div/div[4]/button')
            sleep(1)
            driver.execute_script("arguments[0].click();", button)

            try:
                driver.implicitly_wait(5)
                error = driver.find_element(By.CSS_SELECTOR, '#exch_html > div.xchange_div > div > div.ajax_post_bids_res > div').text
                if "Ошибка" in error:
                    try:
                        input_captcha = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, '//*[@id="exch_html"]/div[2]/div/div[3]/div[2]/input'))
                        )
                        input_captcha.clear()
                        input_captcha.send_keys(captcha_text)
                    except Exception as e:
                        print(f"INPUT CAPCTHA \n{e}")
                        return None

                    button = driver.find_element(By.XPATH, '//*[@id="exch_html"]/div[2]/div/div[4]/button')
                    sleep(1)
                    driver.execute_script("arguments[0].click();", button)
            except:
                pass

            try:
                payment_step = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="exchange_status_html"]/div[3]/div/div[4]/div/a[2]'))
                )
                driver.execute_script("arguments[0].click();", payment_step)
            except Exception as e:
                print(f"PAYMENT STEP ERROR \n{e}")

            try:
                sleep(5)
                new_window = driver.window_handles[1]
                driver.switch_to.window(new_window)

                amount = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '/html/body/div[5]/div/div/div/div[1]/div[2]'))
                )
                amount = amount.text.replace("USDT", "").replace(" ", '')

                address = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '/html/body/div[5]/div/div/div/div[2]/div[2]'))
                )
                address = address.text

                return {
                    "address": address,
                    "amount": amount,
                    "currency": "usdt"
                }
            except Exception as e:
                print(f"DATA ERROR \n{e}")
                return None

        except Exception as e:
            print(f"MONEY ERROR \n{e}")
            return None

def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
