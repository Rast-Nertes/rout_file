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

url = 'https://wh-satano.ru/cheats/apex/spoofer'
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
        driver.implicitly_wait(35)
        a_href = driver.find_element(By.XPATH, '//a[@class="buy-btn"]').get_attribute('href')
        sleep(1)
        driver.get(a_href)
    except Exception as e:
        return {"status": "0", "ext": f"error href{e}"}

    try:
        click(driver, 35, '//*[@id="TypeCurr_titleText"]')
        sleep(1.5)

        driver.implicitly_wait(20)
        choose_tc20 = driver.find_element(By.XPATH, '//span[@class="ddlabel" and text()="USDT"]')
        choose_tc20.click()
        sleep(2.5)
    except Exception as e:
        return {"status": "0", "ext": f"error choose trc20 {e}"}

    try:
        input_data(driver, 20, '//*[@id="email"]', user_email)
        sleep(1.5)
        input_data(driver, 20, '//*[@id="Re_Enter_Email"]', user_email)
        sleep(1.5)
        click(driver, 20, '//*[@id="pay_btn"]')
    except Exception as e:
        return {"status": "0", "ext": f"error submit {e}"}


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            click(driver, 20, '//*[@id="form1"]/section/section/div[2]/div[1]/div[4]')
            sleep(1.5)
        except Exception as e:
            return {"status": "0", "ext": f"error choose {e}"}

        try:
            driver.implicitly_wait(40)
            amount = driver.find_element(By.XPATH, '//*[@id="form1"]/div[3]/div/div[1]/div[2]/span').text.replace(" ", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="form1"]/section/section/div[2]/div[2]/div[4]/div/div[1]/div/span').text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            return {"status": "0", "ext": f"error data  {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
