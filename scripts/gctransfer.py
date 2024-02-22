from time import sleep
from flask import Flask
from flask import jsonify
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#CONSTANS

app = Flask(__name__)
url = 'https://my.gctransfer.info/user/login'
user_login = 'kiracase34@gmail.com'
user_password = 'L7RzGZDNXnF4J2Y'

#CHROME OPTIONS

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

#driver = webdriver.Chrome(options=options)

def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.ID, '__BVID__17')
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.ID, '__BVID__20')
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"DATA ERROR \n{e}")

    try:
        driver.implicitly_wait(20)
        button_login = driver.find_element(By.CSS_SELECTOR, '#app > div > div:nth-child(2) > div > div > div > div > span > form > button')
        driver.execute_script("arguments[0].click();", button_login)
    except Exception as e:
        print(f"BUTTON LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)
        actions = ActionChains(driver)

        try:
            driver.implicitly_wait(10)
            buy_product = driver.find_element(By.CSS_SELECTOR, 'div:nth-child(1) > div > div > div.pl-4.pr-4.mb-4.text-center > button')
            sleep(2.5)
            driver.execute_script("arguments[0].click();", buy_product)
            #На анимацию
            sleep(3)
        except Exception as e:
            print(f"BUY BUTTON ERROR \n{e}")

        #sleep(1000)
        try:
            choose_ = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/form/fieldset[1]/div'))
            )
            choose_.click()
        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")

        for _ in range(2):
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(1)

        actions.send_keys(Keys.ENTER).perform()

        try:
            driver.implicitly_wait(20)
            accept_choose = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/form/button')
            sleep(2)
            driver.execute_script("arguments[0].click();", accept_choose)
        except Exception as e:
            print(f"ACCEPT ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            pay_last_step = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[2]/div/div/div[2]/div/div/form/a')
            pay_last_step = pay_last_step.get_attribute('href')
            sleep(1.5)
            driver.get(pay_last_step)
        except Exception as e:
            print(f'LAST STEP ERROR \n{e}')

        try:
            driver.refresh()
            sleep(5)
            buy_with_trc_20 = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div[2]/div[1]/div[3]/button'))
            )
            sleep(3.5)
            driver.execute_script("arguments[0].click();", buy_with_trc_20)
        except Exception as e:
            print(f"BUY WITH TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(30)
            address = driver.find_element(By.CSS_SELECTOR,
                                          'div.col-span-9.ms-16 > div > div.data-info.pt-12 > div.data-info__address.flex.items-center.justify-between > div > span').text

            driver.implicitly_wait(30)
            amount = driver.find_element(By.CSS_SELECTOR,
                                         'div.total.col-span-12.md\:col-span-6.lg\:col-span-4.hidden.md\:block.dark\:bg-dark-layout > div.total__footer.border-dot.dark\:bg-dark-layout > div:nth-child(1) > span:nth-child(2)').text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }

        except Exception as e:
            print(f"DATA ERROR \n{e}")
            return None

def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
