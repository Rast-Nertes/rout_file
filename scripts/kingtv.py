import requests
from seleniumwire import webdriver
from time import sleep
from flask import Flask, jsonify
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#Acquiring.obmenka

#CONSTANS

user_login = 'kiracase34@gmail.com'
user_password = 'wC$Hp9Ws2#4iLTN'
url = 'https://kingtv.org/'

#API CONSTANS
API_KEY = '7f728c25edca4f4d0e14512d756d6868'
API_URL = 'http://rucaptcha.com/in.php'
API_RESULT_URL = f'http://rucaptcha.com/res.php?key={API_KEY}&action=get'

#PROXY_CONSTANS

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@196.19.121.187:8000",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

#driver = webdriver.Chrome(options= options, seleniumwire_options=proxy_options)


def login(driver):
    driver.get('https://kingtv.org/billing/clientarea.php')
    driver.maximize_window()

    try:
        login_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inputEmail"]'))
        )
        login_input.send_keys(user_login)

        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="inputPassword"]'))
        )
        password_input.send_keys(user_password)

        try:
            button_log_in = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="login"]'))
            )
            button_log_in.click()
        except Exception as e:
            print(f'\n{e}')

    except Exception as e:
        print(f'INPUT ERROR \n{e}')


def get_wallet():
    with webdriver.Chrome(options= options, seleniumwire_options=proxy_options) as driver:
        login(driver)
        driver.get('https://kingtv.org/billing/cart.php?a=confproduct&i=0')

        try:
            check_out = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="product1-order-button"]'))
            )
            check_out.click()

            continue_check_out = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="btnCompleteProductConfig"]'))
            )
            continue_check_out.click()

            check_last = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="checkout"]'))
            )
            check_last.click()
            sleep(2)
        except Exception as e:
            print(f'Check out button ERROR \n{e}')


        try:
            driver.execute_script("window.scrollBy(0, 300);")
            ticket = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="iCheck-accepttos"]'))
            )
            ticket.click()
        except Exception as e:
            print(f'TICKET ERROR \n{e}')


        try:
            driver.set_window_size(200, 300)
            driver.execute_script("window.scrollBy(0, 600);")
            driver.save_screenshot("captcha.png")
            sleep(1)
            driver.maximize_window()
        except:
            pass

        try:
            # Загружаем капчу
            with open('captcha.png', 'rb') as captcha_file:
                data = {
                    'key': API_KEY,
                    'method': 'post'
                }
                response = requests.post(API_URL, data=data, files={'file': captcha_file})
            # Проверяем успешное выполнение капчи
            response_text = response.text.split('|')
            if response_text[0] == "OK":
                captcha_id = response_text[1]
                print(f"Капча успешно отправлена. ID капчи: {captcha_id}")

                # Повторяем запросы для получения результата
                while True:
                    result_response = requests.get(f"{API_RESULT_URL}&id={captcha_id}")
                    if 'OK' in result_response.text:
                        captcha_solution = result_response.text.split('|')[1]
                        print(f"Captcha решена: {captcha_solution}")

                        send_keys_captcha = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, '//*[@id="inputCaptcha"]'))
                        )
                        send_keys_captcha.clear()
                        send_keys_captcha.send_keys(captcha_solution)
                        #driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()

                        click_button = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.XPATH, '//*[@id="btnCompleteOrder"]'))
                        )
                        click_button.click()
                        break

                    elif 'CAPCHA_NOT_READY' in result_response.text:
                        print("Ожидание решения капчи...")
                        sleep(5)
                    else:
                        print("Ошибка при получении результата.")
                        print(result_response.text)
                        break
        except Exception as e:
            print(f"CAPTCHA ERROR \n{e}")


        try:
            pay_now_button = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[1]/div[2]/div[3]/form/input'))
            )
            pay_now_button.click()

        except Exception as e:
            print(f"PAY NOW BUTTON ERROR \n{e}")


        try:
            driver.execute_script("window.scrollTo(0, 800);")

            usdt_choose = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[3]/div[15]/button'))
            )
            usdt_choose.click()

            usdt_20_choose = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[3]/div[2]/button'))
            )
            usdt_20_choose.click()
        except Exception as e:
            print(f'CHOOSE ERROR \n{e}')

        amount = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="step_pay__amount_payTo"]'))
        )
        amount = amount.text

        address = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[7]'))
        )
        address = address.text

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
