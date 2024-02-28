from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://vipstealth.com'
user_login = "kiracase34@gmail.com"
user_password = "kiramira555"

#CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False

def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        actions = ActionChains(driver)
        driver.get('https://vipstealth.com/shop/fake-id-templates/')
        driver.maximize_window()

        try:
            driver.implicitly_wait(10)
            select = driver.find_element(By.XPATH, '//*[@id="doc-type"]')
            select.click()

            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(1)
            actions.send_keys(Keys.ENTER).perform()
            sleep(1)
        except Exception as e:
            print(f"SELECT ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            add_to_cart = driver.find_element(By.CSS_SELECTOR, 'div.single_variation_wrap > div > div.woocommerce-variation-add-to-cart.variations_button.woocommerce-variation-add-to-cart-enabled > a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", add_to_cart)
        except Exception as e:
            print(f"ADD TO CART ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            view_cart = driver.find_element(By.CSS_SELECTOR, 'div.single_variation_wrap > div > div.woocommerce-variation-add-to-cart.variations_button.woocommerce-variation-add-to-cart-enabled > a.button.-button-preview-cart')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", view_cart)

            driver.implicitly_wait(10)
            proceed_to_checkout_button = driver.find_element(By.CSS_SELECTOR, '#sticky-woo-sidebar > div.vc_col-lg-5.vc_col-md-4.vc_col-sm-12.-sticky-block > div > div > div > a')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", proceed_to_checkout_button)
        except Exception as e:
            print(f"CHECKOUT ERROR \n{e}")

        try:
            driver.implicitly_wait(30)
            input_email = driver.find_element(By.ID, 'billing_email')
            input_email.send_keys(user_login)

            driver.implicitly_wait(20)
            input_username = driver.find_element(By.ID, 'billing_company')
            input_username.send_keys("Kira")

            driver.implicitly_wait(10)
            tg = driver.find_element(By.ID, 'contact')
            tg.send_keys("@sobaka")
        except Exception as e:
            print(f"INPUT ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            terms = driver.find_element(By.ID, 'terms')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", terms)

            driver.implicitly_wait(10)
            place_order = driver.find_element(By.ID, 'place_order')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", place_order)
        except Exception as e:
            print(f"TICKET ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            select_currency = driver.find_element(By.CSS_SELECTOR,
                                                  'div.invoice__steps > div.choose-currency-step > div.currencies-select > div')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", select_currency)

            driver.implicitly_wait(10)
            choose_trc20 = driver.find_element(By.CSS_SELECTOR,
                                               'div.currencies-dropdown.currencies-select__body.currencies-select__body_animate > div.currencies-dropdown__content > ul > li:nth-child(2)')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            driver.implicitly_wait(10)
            next_step = driver.find_element(By.CSS_SELECTOR,
                                            'div.invoice__content > div.invoice__steps > div.choose-currency-step > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step)
        except Exception as e:
            print(f"SELECT TRC20 ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH,
                                         '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]').text.replace(
                "USDT", '').replace(" ", '').replace("\nTRX", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH,
                                          '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[1]').text

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
