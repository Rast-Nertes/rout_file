from time import sleep
from flask import jsonify
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


#CONSTANS

url = 'https://cbilling.eu/index.php?mode=auth'
user_login = 'ab662c1'
user_password = 'a40d37a'

#PROXY_CONSTANS

proxy_address = "45.142.31.82"
proxy_login = 'EeHUrd'
proxy_password = 'xBJeLY'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:8000",
        "https":f"http://{proxy_login}:{proxy_password}@{proxy_address}:8000"
    }
}

#CHROME OPTIONS

options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("--disable-save-password-bubble")


def login(driver):
    try:
        print("LOGIN START")
        driver.get(url)
        driver.maximize_window()
        element_start__input_user_login = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, '/html/body/section/div/div/div[1]/div/div[2]/form/div[1]/input'))
        )
        element_start__input_user_login.send_keys(user_login)

        input_user_password = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/section/div/div/div[1]/div/div[2]/form/div[2]/input'))
        )
        input_user_password.send_keys(user_password)

        accept_login = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/section/div/div/div[1]/div/div[2]/form/input[2]'))
        )
        accept_login.click()

    except Exception as e:
        print(f"LOGIN ERROR -- {e}")


def get_wallet():
    with webdriver.Chrome(seleniumwire_options=proxy_options, options=options) as driver:
        login(driver)
        try:
            driver.get('https://cbilling.eu/?mode=ballance')
            
            try:
                choose_wallet = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, '//input[@value="cryptocloud"]'))
                )
                choose_wallet.click()
            except:
                driver.implicitly_wait(10)
                find_input_tag = driver.find_element(By.XPATH, '/html/body/section/div/div/div[1]/div/div[2]/form/div[1]/input')
                if find_input_tag:
                    return {"status": "0", "ext": "Login error. Check script."}
            
            accept_wallet = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div/div/div[1]/form/input'))
            )
            accept_wallet.click()

            new_window = driver.window_handles[1]
            driver.switch_to.window(new_window)

            sleep(17)
            print("PAY START")
            #Ждем, когда кнопка прогрузится
            pay_ru_ = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div[3]/button/span'))
            )
            pay_ru_.click()

            amount = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.amount-clipboard span.text-18'))
            )
            amount = amount.text.replace("USDT", "").replace(" ", '')

            address = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.address-clipboard span.text-10'))
            )
            address = address.text

            return {
                "address":address,
                "amount":amount,
                "currency":"usdt"
            }
        except Exception as e:
            print(f"WALLET ERROR -- {e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
