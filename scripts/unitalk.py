from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from flask import Flask, jsonify
from twocaptcha import TwoCaptcha
from selenium import webdriver
from time import sleep

#thedex.cloud

#CONSTANS
app = Flask(__name__)
user_login = 'kiracase34@gmail.com'
user_password = '0WvpZNBM'
url = 'https://my.unitalk.cloud/enter.html#auth'

#API CONSTANS
api_key = '7f728c25edca4f4d0e14512d756d6868'
site_key = '6LdTrQYeAAAAAB5wwjOovTVSrXDmPB7we-9dYi0o'

# driver = webdriver.Chrome()
# driver.maximize_window()

def solve_captcha(sitekey: str, url: str) -> str:
    solver = TwoCaptcha(api_key)
    result = solver.recaptcha(sitekey=sitekey, url=url, invisible=1)
    return result["code"]

def captcha_and_login(driver):
    driver.get(url)
    driver.maximize_window()
    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/input')
        input_email.clear()
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[3]/input')
        input_password.clear()
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        driver.implicitly_wait(30)
        captcha_result = solve_captcha(sitekey=site_key, url=url)
        print(captcha_result)

        driver.execute_script(f'var textarea = document.getElementById("g-recaptcha-response-100000"); textarea.style.display = "block"; textarea.innerHTML = "{captcha_result}";')
    except:
        pass

    try:
        driver.implicitly_wait(10)
        button_login = driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[2]/div[6]/button')
        driver.execute_script("arguments[0].click();", button_login)
    except Exception as e:
        print(f"BUTTON ERROR \n{e}")
    sleep(5)

def get_wallet():
    with webdriver.Chrome() as driver:
        captcha_and_login(driver)
        driver.get('https://my.unitalk.cloud/index.html#balance')

        try:
            driver.implicitly_wait(10)
            input_balance = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[1]/div[2]/div[2]/div/div/label/input')
            input_balance.send_keys('3')
        except Exception as e:
            print(f"INPUT BALANCE ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            add_value = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[1]/div[1]/div[2]/div[2]/div/button')
            driver.execute_script("arguments[0].click();", add_value)
        except Exception as e:
            print(f"ADD VALUE BUTTON \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_payment_method = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[3]/button')
            driver.execute_script("arguments[0].click();", choose_payment_method)

            driver.implicitly_wait(10)
            thedex_choose = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/div[3]/ul/li[2]')
            driver.execute_script("arguments[0].click();", thedex_choose)

            driver.implicitly_wait(10)
            buy_ = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div/button')
            driver.execute_script("arguments[0].click();", buy_)
        except Exception as e:
            print(f"BUY BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            tether_trc20 = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div/div[1]/div/div[1]/div/div[2]/form/div[2]/ul/li[1]')
            driver.execute_script("arguments[0].click();", tether_trc20)

            driver.implicitly_wait(10)
            next_step = driver.find_element(By.XPATH, '//*[@id="btn-sub"]')
            driver.execute_script("arguments[0].click();", next_step)
        except Exception as e:
            print(f"TETHER TRC20 BUTTON ERROR \n{e}")

        amount = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[3]/div[1]/div[2]'))
        )
        amount = amount.text.replace(' USDT TRC20 ', '')

        address = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="app"]/div/div/div/div/div[1]/div/div[1]/div[1]/div[3]/div/div[3]/div[2]/div[2]'))
        )
        address = address.text

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }

@app.route("/api/selenium/unitalk")
def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)

if __name__ == "__main__":
    app.run(use_reloader=False, debug=True, port=5045)