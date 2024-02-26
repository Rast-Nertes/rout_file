from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#PAYMENTARS

#CONSTANS

user_login = 'kiracase34@gmail.com'
user_password = '9eeHhLkJuWTTAKK'
url = 'https://freekurses.site/moj-akkaunt/'

#API CONSTANS
api_key = '7f728c25edca4f4d0e14512d756d6868'

#CHROME CONSTANS
options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.headless = False


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(10)
        input_email = driver.find_element(By.ID, 'username')
        input_email.send_keys(user_login)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.ID, 'password')
        input_password.send_keys(user_password)
    except Exception as e:
        print(f"INPUT DATA ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        login_button = driver.find_element(By.XPATH, '//*[@id="customer_login"]/div[1]/form/p[3]/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN BUTTON ERROR \n{e}")


def get_wallet(driver):
    login(driver)
    driver.get('https://freekurses.site/product/natalja-minina-osobennosti-sevooborota-na-ovoshhah-2024/')
    try:
        driver.implicitly_wait(20)
        button_in_busket = driver.find_element(By.XPATH, '//*[@id="product-523205"]/div[2]/form/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", button_in_busket)
    except Exception as e:
        print(f"ADD TO BUSKET ERROR \n{e}")

    driver.get('https://freekurses.site/wishlist/cart/')

    try:
        driver.implicitly_wait(20)
        input_count = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/main/article/div/div/form/table/tbody/tr[1]/td[5]/div/input')
        sleep(2)
        input_count.clear()
        input_count.send_keys('1')
    except Exception as e:
        print(f"INPUT COUNT ERROR \n{e}")

    try:
        driver.implicitly_wait(10)
        refresh_busket = driver.find_element(By.XPATH, '//*[@id="post-57"]/div/div/form/table/tbody/tr[2]/td/button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", refresh_busket)
    except Exception as e:
        print(f"REFRESH BUSKET \n{e}")

    sleep(1.5)
    driver.get('https://freekurses.site/wishlist/checkout/')


def choose_payment_method():
    with webdriver.Chrome(options=options) as driver:
        get_wallet(driver)

        try:
            driver.implicitly_wait(10)
            choose_crypto_cloud_payment = driver.find_element(By.XPATH, '//*[@id="payment"]/ul/li[12]/label')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_crypto_cloud_payment)
        except Exception as e:
            print(f"CHOOSE CRYPTO ERROR \n{e}")

        try:
            driver.implicitly_wait(10)
            accept_choose = driver.find_element(By.ID, 'place_order')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", accept_choose)
        except Exception as e:
            print(f"ACCEPT CHOOSE ERROR")

        try:
            driver.implicitly_wait(30)
            buy_with_trc_20 = driver.find_element(By.CSS_SELECTOR, 'div.total.col-span-12.md\:col-span-6.lg\:col-span-4.hidden.md\:block.dark\:bg-dark-layout > div.total__footer.border-dot.dark\:bg-dark-layout > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_with_trc_20)

            driver.implicitly_wait(10)
            buy_with_trc = driver.find_element(By.CSS_SELECTOR, 'div.total.col-span-12.md\:col-span-6.lg\:col-span-4.hidden.md\:block.dark\:bg-dark-layout > div.total__footer.border-dot.dark\:bg-dark-layout > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_with_trc)
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
    wallet_data = choose_payment_method()
    print(wallet_data)
    return jsonify(wallet_data)
