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
app = Flask(__name__)
user_login = 'kiracase34@gmail.com'
user_password = 'qnCH7mNd'
url = 'https://proxys.io/ru/user/login'

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
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")

#driver = webdriver.Chrome(options= options, seleniumwire_options=proxy_options)

def captcha_and_login(driver):
    driver.get(url)

    try:
        input_email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="login-form-login"]'))
        )
        input_email.send_keys(user_login)

        input_password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="login-form-password"]'))
        )
        input_password.send_keys(user_password)

        try:
            delete_block = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[5]'))
            )
            driver.execute_script("arguments[0].remove();", delete_block)

            delete_block_2 = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[4]'))
            )
            driver.execute_script("arguments[0].remove();", delete_block_2)

        except:
            print("ERROR DELETE")

    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        try:
            message_help = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="login-form-captcha"]'))
            )
            message_help.send_keys("Please, help")
        except:
            pass

        driver.set_window_size(300, 400)
        driver.execute_script("window.scrollBy(0, 210);")
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
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="login-form-captcha"]'))
                    )
                    send_keys_captcha.clear()
                    send_keys_captcha.send_keys(captcha_solution)
                    #driver.find_element(By.XPATH, '//*[@id="login-form"]/button').click()

                    click_button = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="login-form"]/button'))
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
        # Для авторизации
        sleep(10)
    except Exception as e:
        print(f"CAPTCHA ERROR \n{e}")
        return None
    #sleep(5)
def get_wallet():
    with webdriver.Chrome(options= options, seleniumwire_options=proxy_options) as driver:
        captcha_and_login(driver)
        driver.get('https://proxys.io/ru/cart')
        actions = ActionChains(driver)
        try:
            ind_ipv4 = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="accordion"]/div[1]/div[1]'))
            )
            ind_ipv4.click()
            #Время для анимации
            sleep(2)

            driver.execute_script("window.scrollBy(0, 100);")
        except Exception as e:
            print(f'IPv4 ERROR \n{e}')

        try:
            select_county = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="ip4paymentform-country"]'))
            )
            select_county.click()

            actions.send_keys(Keys.ARROW_DOWN).perform()
            actions.send_keys(Keys.ENTER).perform()
        except Exception as e:
            print(f"COUNTRY ERROR \n{e}")

        try:
            ticket = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="ip4paymentform-terms"]'))
            )
            ticket.click()
        except Exception as e:
            print(f'TICKET ERROR\n{e}')

        try:
            choose_crypto_currency = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="ip4-payment-form"]/div/div[2]/div/div/div[2]/div[1]/div[1]/div/span/span[1]/span'))
            )
            choose_crypto_currency.click()

            sleep(1)

            actions.send_keys(Keys.ARROW_DOWN).perform()
            actions.send_keys(Keys.ENTER).perform()
        except Exception as e:
            print(f"CHOOSE CRYPTO CURRENCY ERROR\n{e}")

        try:
            continue_payment = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="ip4-payment-form"]/div/div[2]/div/div/div[2]/div[2]/button'))
            )
            continue_payment.click()
        except Exception as e:
            print(f'CONTINUE BUTTON ERROR\n{e}')

        try:
            driver.implicitly_wait(10)
            choose_currency = driver.find_element(By.CSS_SELECTOR, 'div.content__actions > div > div.css-bb03bc > div:nth-child(1) > div.css-veoc3i.e1656iwc8')
            driver.execute_script("arguments[0].click();", choose_currency)

            driver.implicitly_wait(10)
            select_network = driver.find_element(By.CSS_SELECTOR, '#downshift-10-item-0')
            driver.execute_script("arguments[0].click();", select_network)
        except Exception as e:
            print(f'CHOOSE USDT ERROR\n{e}')

        try:
            driver.implicitly_wait(10)
            select_net = driver.find_element(By.CSS_SELECTOR, 'div.pay__content > div > div.content__actions > div > div.css-bb03bc > div:nth-child(2) > div.css-veoc3i.e1656iwc8')
            driver.execute_script("arguments[0].click();", select_net)

            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.CSS_SELECTOR, '#downshift-11-item-5 > div')
            driver.execute_script("arguments[0].click();", choose_trc20)
        except Exception as e:
            print(f"CHOOSE TRC20 \n{e}")

        try:
            driver.implicitly_wait(10)
            pay_button = driver.find_element(By.CSS_SELECTOR, 'div.pay__content > div > div.content__actions > div > button')
            driver.execute_script("arguments[0].click();", pay_button)
        except Exception as e:
            print(f"PAY BUTTON ERROR \n{e}")

        amount = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="createForm"]/section[2]/div/div/div[1]/div[2]/div[6]/p'))
        )
        amount = amount.text.replace("USDT", "")

        address = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="createForm"]/section[2]/div/div/div[1]/div[2]/div[4]/p'))
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
