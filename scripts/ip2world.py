import random
from time import sleep
from flask import Flask, jsonify
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CONSTANTS
app = Flask(__name__)
url = 'https://client.ipidea.io'
user_login = 'kiracase34@gmail.com'
user_password = 'KKKmmm12'
# CHROME OPTIONS
chrome_options = webdriver.ChromeOptions()
user_agent = UserAgent()
chrome_options.add_argument(f"user-agent={user_agent.random}")
#driver = webdriver.Chrome(options=chrome_options)

def login(driver):
    try:
        print("LOGIN START")
        driver.get('https://www.ip2world.com/login/?pat=/')
        driver.maximize_window()
        try:
            close = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="activity_close"]/img[1]'))
            )
            close.click()
        except:
            pass

        try:
            accept = driver.find_element(By.XPATH, '//*[@id="cookie_prompt_btn"]')
            driver.execute_script("arguments[0].click();", accept)
        except:
            pass

        try:
            # sleep(2)
            login_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="login_phone"]'))
            )
            login_input.send_keys(user_login)
        except Exception as e:
            print(f"ERROR LOGIN INPUT -- {e}")

        try:
            password_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="login_password"]'))
            )
            password_input.send_keys(user_password)
        except Exception as e:
            print(f"ERROR PASS INPUT -- {e}")
        driver.execute_script("window.scrollBy(0, 400);")
        try:
            log_in = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="login"]'))
            )
            log_in.click()
        except Exception as e:
            print(f"BUTTON ERROR \n{e}")
        try:
            driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div[1]/img').click()
        except:
            pass

    except Exception as e:
        print(f"LOGIN ERROR -- {e}")

def get_wallet_data():
    try:
        with webdriver.Chrome(options=chrome_options) as driver:
            login(driver)
        #Слип, чтобы перейти на сайт
            sleep(1.5)
            driver.get('https://www.ip2world.com/residential/')

            try:
                buy_plan = WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="residential__plan_package"]/div[2]/div[1]/div/div[3]/button'))
                )
                buy_plan.click()
            except Exception as e:
                print(f"BUY PLAN BUTTON ERROR - \n{e}")


            try:
                close = driver.find_element(By.XPATH, '//*[@id="activity_close"]/img[2]')
                driver.execute_script("arguments[0].click();", close)
            except:
                pass

            sleep(3)
            new_window = driver.window_handles[1]
            driver.switch_to.window(new_window)
            driver.execute_script("window.scrollBy(0, 350);")

            try:
                virtual_wallet = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="coin_pay"]/div[1]'))
                )
                virtual_wallet.click()
            except Exception as e:
                print(f"VIRTUAL WALLET ERROR -- \n{e}")

            try:
                buy_ =WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH , '//*[@id="coin_pay"]/div[2]/div[2]/div[2]/div[2]/button'))
                )
                buy_.click()
            except Exception as e:
                print(f"BUY ERROR \n{e}")

            sleep(5)
            new_window = driver.window_handles[2]
            driver.switch_to.window(new_window)

            trc_20 = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[1]/div[2]/div/div[1]'))
            )
            trc_20.click()

            sleep(2.5)
            driver.execute_script("window.scrollBy(0, 300);")

            amount = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[1]/div[3]/div[7]/div[2]/div[1]/p/i'))
            )
            amount = amount.text.replace("USDT", "")

            address = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located(
                    (By.XPATH, '/html/body/div[3]/div[2]/div[2]/div[1]/div[3]/div[7]/div[1]/div[1]/p'))
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
    #print(wallet_data)
    return jsonify(wallet_data)
