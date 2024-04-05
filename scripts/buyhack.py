from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://www.buyhack.pro/en/products/apex-legends/mason-apex'
user_email = "yewoxo4550@otemdi.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    driver.execute_script("arguments[0].click();", elem_click)


def input_data(driver, time, XPATH, data):
    driver.implicitly_wait(time)
    elem_input = driver.find_element(By.XPATH, XPATH)
    elem_input.clear()
    elem_input.send_keys(data)


def login(driver):
    actions = ActionChains(driver)
    driver.get(url)
    driver.maximize_window()

    try:
        click(driver, 35, '/html/body/main/section/div/div[2]/div[2]/div/form/div[4]/div[1]/label/span')
        sleep(1)
        click(driver, 20, '/html/body/main/section/div/div[2]/div[2]/div/form/div[4]/div[2]/label/span')
        sleep(2.5)
        click(driver, 20, '/html/body/main/section/div/div[2]/div[2]/div/form/button')
    except Exception as e:
        print(f"ERROR TICKETS \n{e}")

    # try:
    #     click(driver, 35, '//*[@id="TypeCurr_titleText"]')
    #     sleep(1.5)
    #
    #     driver.implicitly_wait(20)
    #     choose_tc20 = driver.find_element(By.XPATH, '//span[@class="ddlabel" and text()="USDT"]')
    #     choose_tc20.click()
    #     sleep(2.5)
    # except Exception as e:
    #     print(f"ERROR CHOOSE TRC20 \n{e}")

    try:
        input_data(driver, 20, '//*[@id="email"]', user_email)
        sleep(1)
        input_data(driver, 20, '//*[@id="Re_Enter_Email"]', user_email)
        sleep(1)
        click(driver, 20, '//*[@id="pay_btn"]')
    except Exception as e:
        print(f'ERROR SUBMIT \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(40)
            amount = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]').text.replace(" ", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div[1]').text

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
