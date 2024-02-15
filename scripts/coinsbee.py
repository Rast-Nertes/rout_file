import requests
from seleniumwire import webdriver
from time import sleep
from flask import Flask, jsonify
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

#COINSGATE

#CONSTANS

app = Flask(__name__)
url = 'https://www.coinsbee.com/ru/login'
user_login = 'kiracase34@gmail.com'
user_password = 'kiramira55'

#API CONSTANS

API_KEY = '7f728c25edca4f4d0e14512d756d6868'
API_URL = 'http://rucaptcha.com/in.php'
API_RESULT_URL = f'http://rucaptcha.com/res.php?key={API_KEY}&action=get'

#CHROME OPTIONS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.headless = False
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

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


#driver = webdriver.Chrome(options=options, seleniumwire_options=proxy_options)
def captcha(driver):
    driver.get(url)
    driver.maximize_window()
    try:
        input_email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="email"]'))
        )
        input_email.send_keys(user_login)

        input_password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="password"]'))
        )
        input_password.send_keys(user_password)

    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        driver.set_window_size(200, 300)
        driver.execute_script("window.scrollBy(0, 350);")
        sleep(1)
        try:
            message_to_help = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="c"]'))
            )
            message_to_help.send_keys("Решите капчу")
        except:
            pass
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

                    send_keys_captcha = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="c"]'))
                    )
                    send_keys_captcha.clear()
                    send_keys_captcha.send_keys(captcha_solution)
                    driver.find_element(By.XPATH, '/html/body/div/div/section/div/div/form/button').click()

                    click_button = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/section/div/div/form/button'))
                    )
                    click_button.click()
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
    except Exception as e:
        print(f'Капчи нет.')
        sleep(2)

def get_wallet():
    with (webdriver.Chrome(options= options, seleniumwire_options= proxy_options) as driver):
        captcha(driver)
        actions = ActionChains(driver)
        driver.get('https://www.coinsbee.com/ru/Steam-bitcoin')
        driver.execute_script("window.scrollBy(0, 200);")
        try:
            try:
                sleep(2)
                choose_tether = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/div/div/input'))
                )
                choose_tether.click()
            except Exception as e:
                print(f"tether click error \n{e}")

            # actions.send_keys(Keys.ARROW_DOWN).perform()
            # sleep(0.5)
            #actions.send_keys(Keys.ENTER).perform()
            click_tether = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/div/div[2]'))
            )
            click_tether.click()
        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")

        try:
            add_to_busket = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="addtocartbutton"]/div/a[2]'))
            )
            add_to_busket.click()

            path_to_busket = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="shop_modal"]/div/div/div[3]/a'))
            )
            path_to_busket.click()
        except Exception as e:
            print(f"ADD ERROR \n{e}")

        try:
            try:
                email_ = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '/html/body/div/div/div[5]/div/div/form/div[1]/div/input'))
                )
                email_.send_keys(user_login)
                print("INPUT EMAIL ERROR")
            except Exception as e:
                pass

            make_application = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="checkoutform"]/div/button/span'))
            )
            make_application.click()

            buy_now = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="btnBuyCoingate"]'))
            )
            buy_now.click()
        except Exception as e:
            print(f"APPLICATION ERROR \n{e}")

        try:
            amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="app"]/div/div/div[2]/div[2]/div[1]/div[1]/div[2]/div/div[2]/span[2]/span[1]'))
            )
            amount = amount.text.replace("USDT", "")

            address = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '//*[@id="app"]/div/div/div[1]/div/div[1]/div[1]/div[2]/div[3]/div[2]/div[2]/span'))
            )
            address = address.text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")

def wallet():
    wallet_data = get_wallet()
    return jsonify(wallet_data)

