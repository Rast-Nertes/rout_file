from time import sleep
from flask import Flask
import pyautogui
from flask import jsonify
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#CONSTANS

app = Flask(__name__)
url = 'https://brainlabz.ru/product/nolvadex-tamoxifen-10mg-60-tabs-600mg/'
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

def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        actions = ActionChains(driver)
        driver.get(url)
        driver.maximize_window()

        try:
            driver.implicitly_wait(10)
            add_to_cart_button = driver.find_element(By.CSS_SELECTOR, 'div.product-info.summary.col-fit.col.entry-summary.product-summary > form > button')
            sleep(1)
            driver.execute_script("arguments[0].click();", add_to_cart_button)
        except Exception as e:
            print(f'ADD TO CART ERROR \n{e}')

        driver.get('https://brainlabz.ru/checkout/')

        try:
            driver.implicitly_wait(10)
            input_first_name = driver.find_element(By.ID, 'billing_first_name')
            sleep(1)
            input_first_name.send_keys('1111111')

            driver.implicitly_wait(10)
            input_second_name = driver.find_element(By.ID, 'billing_last_name')
            input_second_name.send_keys('1111111111')

        except Exception as e:
            print(f"NAME`S ERROR INPUT \n{e}")

        try:
            driver.implicitly_wait(10)
            input_address = driver.find_element(By.ID, 'billing_address_1')
            input_address.send_keys('111111111111')

            driver.implicitly_wait(10)
            input_address_2 = driver.find_element(By.ID, 'billing_address_2')
            input_address_2.send_keys('11111111111111')
        except Exception as e:
            print(f"INPUT ADDRESS ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_city = driver.find_element(By.ID, 'billing_city')
            input_city.send_keys('11111111111')

        except Exception as e:
            print(f"INPUT CITY ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            choose_state_coutry = driver.find_element(By.ID, 'select2-billing_state-container')
            sleep(2)
            choose_state_coutry.click()

            sleep(2)
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.5)
            actions.send_keys(Keys.ENTER).perform()
        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_post_code = driver.find_element(By.ID, 'billing_postcode')
            input_post_code.send_keys('111111111')
        except Exception as e:
            print(f"INPUT POST CODE ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_phone = driver.find_element(By.ID, 'billing_phone')
            input_phone.send_keys("1")
        except Exception as e:
            print(f"INPUT PHONE ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            input_email = driver.find_element(By.ID, 'billing_email')
            input_email.send_keys("2222222@gmail.com")
        except Exception as e:
            print(f"INPUT EMAIL ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            checkbox = driver.find_element(By.ID, 'ship-to-different-address-checkbox')
            driver.execute_script("arguments[0].click();", checkbox)
        except Exception as e:
            print(f"CHECKBOX ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            place_order_button = driver.find_element(By.ID, 'place_order')
            driver.execute_script("arguments[0].click();", place_order_button)
        except Exception as e:
            print(f"PLACE ORDER ERROR \n{e}")

        try:
            pay_ = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.total__footer.border-dot.dark\:bg-dark-layout > button'))
            )
            driver.execute_script("arguments[0].click();", pay_)
        except Exception as e:
            print(f"PAY BUTTON ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            amount = driver.find_element(By.CSS_SELECTOR,
                                          'div.total__footer.border-dot.dark\:bg-dark-layout > div:nth-child(1) > span:nth-child(2)').text.replace("USDT", '').replace(" ", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR,
                                         'div.data-info.pt-12 > div.data-info__address.flex.items-center.justify-between > div > span').text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            print(f"DATA ERROR \n{e}")

def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
