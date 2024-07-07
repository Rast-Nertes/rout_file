import pyautogui
from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://ru.wankzvr.com/join?src_element=sale_strip&src_location=global'
user_name = "rwork875"
user_email_2 = "rwork875@gmail.com"
user_password = "332144ek1134"

# CHROME CONSTANS

proxy_address = "196.19.121.187"
proxy_login = 'WyS1nY'
proxy_password = '8suHN9'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1)
    driver.execute_script("arguments[0].click();", elem_click)
    sleep(1)


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
        click(driver, 20, '/html/body/div[2]/div/div/div/a')
    except:
        pass

    try:
        click(driver, 20, '//*[@id="main"]/div/section[1]/section/div[1]/div[2]/div[1]/div/div[2]/span')
    except Exception as e:
        print(f'ERROR CHOOSE PLAN \n{e}')

    try:
        click(driver, 30, '//*[@id="main"]/div/section[1]/form/div/div[2]/div[1]/div[1]/div[2]/a[2]')
    except Exception as e:
        print(f"ERROR CHOOSE BIT \n{e}")

    try:
        driver.implicitly_wait(30)
        input_name = driver.find_element(By.XPATH, '//*[@id="main"]/div/section[1]/form/div/div[2]/div[1]/div[2]/div[2]/div[1]/input')
        sleep(1.5)
        input_name.send_keys(user_name)

        driver.implicitly_wait(30)
        input_email = driver.find_element(By.XPATH, '//*[@id="main"]/div/section[1]/form/div/div[2]/div[1]/div[2]/div[2]/div[2]/input')
        sleep(1.5)
        input_email.send_keys(user_email_2)

        driver.implicitly_wait(30)
        input_pass = driver.find_element(By.XPATH, '//*[@id="main"]/div/section[1]/form/div/div[2]/div[1]/div[2]/div[2]/div[3]/input')
        sleep(1.5)
        input_pass.send_keys(user_password)
    except Exception as e:
        print(f"ERROR INPUT DATA \n{e}")

    try:
        click(driver, 40, '//*[@id="main"]/div/section[1]/form/div/div[2]/div[1]/div[2]/div[2]/button')
    except Exception as e:
        print(f"ERROR LOG BUTTON \n{e}")

    try:
        click(driver, 40, '//*[@id="coin_label_USDT"]')
        sleep(1)
        click(driver, 20, '//*[@id="wrapper"]/div[1]/div/div[1]/div[5]/fieldset/div/div/div[1]/label[1]')
    except Exception as e:
        print(f"ERROR CHOOSE TRC20 \n{e}")

    try:
        driver.implicitly_wait(30)
        choose_tariff = driver.find_element(By.ID, 'px')
        choose_tariff.click()
        sleep(1)

        actions.send_keys(Keys.ARROW_UP).perform()
        sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()
    except Exception as e:
        print(f'ERROR CHOOSE TARIFF \n{e}')

    try:
        click(driver, 20, '//*[@id="submit"]')
    except Exception as e:
        print(f"ERROR ACCEPT TRANS \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(90)
            amount = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[1]/div[2]/div/div[1]').text.replace("USDT", '').replace(" ", '').replace("TRX", '').replace("\n", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="payment-page"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/div[2]/div[2]/div/div[1]').text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:
            return {"status":"0", "ext":f"error data {e}"}


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
