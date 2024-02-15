import requests
from time import sleep
from flask import Flask
from flask import jsonify
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#CONSTANS

app = Flask(__name__)
url = 'https://smmlaboratory.com'
user_login = 'kiracase34@gmail.com'
user_password = 'kirakira123'

#API CONSTANS

API_KEY = '7f728c25edca4f4d0e14512d756d6868'
API_URL = 'http://rucaptcha.com/in.php'
API_RESULT_URL = f'http://rucaptcha.com/res.php?key={API_KEY}&action=get'

#CHROME OPTIONS

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

#driver = webdriver.Chrome(options=chrome_options)
def captcha(driver):
    try:
        driver.get(url)
        #captcha_image_element = driver.find_element(By.ID, 'captcha_image')
        captcha_image_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'captcha_image'))
        )
        captcha_image_url = captcha_image_element.get_attribute('src')
        driver.set_window_size(200, 300)
        driver.execute_script("window.scrollBy(0, 200);")
        driver.save_screenshot("captcha.png")
        sleep(2)
        driver.maximize_window()

        #Загружаем капчу
        with open('captcha.png', 'rb') as captcha_file:
            data = {
                'key':API_KEY,
                'method':'post'
            }
            response = requests.post(API_URL, data = data, files={'file':captcha_file})

        sleep(3)
        #Проверяем успешное выполнение капчи
        response_text = response.text.split('|')
        if response_text[0] == "OK":
            captcha_id = response_text[1]
            print(f"Капча успешно отправлена. ID капчи: {captcha_id}")

            #Повторяем запросы для получения результата
            while True:
                result_response = requests.get(f"{API_RESULT_URL}&id={captcha_id}")
                if 'OK' in result_response.text:
                    captcha_solution = result_response.text.split('|')[1]
                    print(f"Captcha решена: {captcha_solution}")

                    #driver.find_element(By.XPATH, '//*[@id="captcha_input"]').send_keys(captcha_solution)
                    #driver.find_element(By.XPATH, '//*[@id="submit_button"]').click()
                    send_keys_captcha = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="captcha_input"]'))
                    )
                    send_keys_captcha.send_keys(captcha_solution)
                    driver.find_element(By.XPATH, '//*[@id="submit_button"]').click()
                    break

                elif 'CAPCHA_NOT_READY' in result_response.text:
                    print("Ожидание решения капчи...")
                    sleep(5)  # Подождите некоторое время перед повторным запросом
                else:
                    print("Ошибка при получении результата.")
                    print(result_response.text)
                    break
        else:
            print(f"Ошибка при отправке капчи. Ответ сервера: {response.text}")
    except:
        print('Капчи нет.')
        driver.maximize_window()
        sleep(2)

def login(driver):
    captcha(driver)
    #Проверим, правильно ли ввели капчу с первого раза.

    try:
        captcha_image_element = driver.find_element(By.ID, 'captcha_image')
        print("Капча была введена неверно.")
        captcha()
    except:
        print("Капча была введена верно.")

    try:
        print("LOGIN START")
        #Клик для входа
        element_click = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="accaunt"]'))
        )
        element_click.click()

        #Вводим логин

        element_start__input_user_login = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.ID, 'email'))
        )
        element_start__input_user_login.send_keys(user_login)

        #Вводим пароль

        input_user_password = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'password'))
        )
        input_user_password.send_keys(user_password)

        #Заходим

        accept_registration = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="register-box"]/div[1]/button[1]'))
        )
        accept_registration.click()

        sleep(5)

        print("LOGIN SUCCEFUL")

    except Exception as e:
        print(f"LOGIN ERROR -- \n{e}")

def get_wallet_data():
    try:
        with webdriver.Chrome(options=chrome_options) as driver:
            login(driver)
            print("WALLET DATA START")

            driver.get('https://smmlaboratory.com/money/wallet/')

            add_to_cart = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[9]/div[2]/div[2]/div[4]/button'))
            )
            add_to_cart.click()

            basket = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/nav/a[2]/div[1]'))
            )
            basket.click()

            driver.execute_script("window.scrollBy(0, 700);")


            method_of_payment = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="for-button-submit"]/div[3]/div/label[2]/div'))
            )
            method_of_payment.click()

            sleep(5)

            order_ = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div[9]/div/div/div[4]/div[1]/input'))
            )
            order_.click()

            choose_wallet = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[1]/div[3]/div[1]/div/div'))
            )
            choose_wallet.click()

            choose_trc20 = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[1]/div[3]/div[1]/div[2]/div[2]/ul/li[2]/div'))
            )
            choose_trc20.click()

            next_step = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[1]/div[3]/button'))
            )
            next_step.click()

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
        print(f"GET WALLET ERROR -- \n{e}")
        return None

def wallet():
    wallet_data = get_wallet_data()
    return jsonify(wallet_data)
