from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from flask import Flask, jsonify
from twocaptcha import TwoCaptcha
from selenium import webdriver
from time import sleep

#Freekassa

#CONSTANS
app = Flask(__name__)
user_login = 'kiracase34@gmail.com'
user_password = '-q?9My75vp2i!*w'
url = 'https://hstock.org/ru/login'

#API CONSTANS
api_key = '7f728c25edca4f4d0e14512d756d6868'
site_key = '6Lf2fMEUAAAAABevtkQPJ7MCJMtMbyWmqCIbuN4p'

#driver = webdriver.Chrome()

def solve_captcha(sitekey: str, url: str) -> str:
    solver = TwoCaptcha(api_key)
    result = solver.recaptcha(sitekey=sitekey, url=url, invisible=1)
    return result["code"]

def captcha_and_login(driver):
    driver.get("https://hstock.org/ru")
    driver.maximize_window()

    try:
        go_to_log = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/header/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/a'))
        )
        go_to_log.click()
    except Exception as e:
        print(f"BUTTON GO TO LOG ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        accept_all = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/div/div[2]/button[1]')
        accept_all.click()
    except:
        pass

    driver.implicitly_wait(30)
    captcha_result = solve_captcha(sitekey=site_key, url=url)
    print(captcha_result)

    driver.execute_script(f'var textarea = document.getElementById("g-recaptcha-response-100000"); textarea.style.display = "block"; textarea.innerHTML = "{captcha_result}";')

    try:
        input_email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'email'))
        )
        input_email.send_keys(user_login)

        input_pass = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, 'password'))
        )
        input_pass.send_keys(user_password)
    except Exception as e:
        print(f'ERROR INPUT \n{e}')
        return None

    try:
        button_click_to_login = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'login-button'))
        )
        button_click_to_login.click()
    except Exception as e:
        print(f"ERROR BUTTON LOGIN \n{e}")
        return None


def get_wallet():
    with webdriver.Chrome() as driver:
        captcha_and_login(driver)
        try:
            append_money = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/header/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/a/span/span'))
            )
            append_money.click()
        except Exception as e:
            print(f"APPEND ERROR \n{e}")

        try:
            choose_trc20 = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/header/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[1]/div[3]/div[2]/ul/li[7]'))
            )
            choose_trc20.click()
        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")
            return None

        try:
            driver.implicitly_wait(3)
            driver.find_element(By.XPATH, '//*[@id="header-box"]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/button').click()
        except Exception as e:
            pass

        try:
            input_summ = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="header-box"]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/form/div[1]/div[3]/input'))
            )
            input_summ.send_keys('920')

            try:
                amount = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/header/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/form/div[2]/div[1]/div[2]'))
                )
                amount = amount.text.replace('Tether USDT (trc20)', '').replace(' ', '')
                print(amount)
               # sleep(20)
            except Exception as e:
                print(f"AMOUNT ERROR \n{e}")
                return None

            buy_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="header-box"]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/form/div[2]/div[2]/button'))
            )
            buy_button.click()

        except Exception as e:
            print(f'INPUT SUMM ERROR \n{e}')
            return None

        try:
            adress = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="header-box"]/div/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div[2]/div/div[2]/div/div/form/div/div[4]/div[2]/div'))
            )
            address = adress.get_attribute('value')
        except Exception as e:
            print(f'DATA ERROR \n{e}')
            return None

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }

@app.route("/api/selenium/hstock")
def hstock():
    wallet_data = get_wallet()
    #print(wallet_data)
    return jsonify(wallet_data)

if __name__ == "__main__":
    #hstock()
    app.run(use_reloader=False, debug=True, port=5035)