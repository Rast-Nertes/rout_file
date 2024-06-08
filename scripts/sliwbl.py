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

url = 'https://s2.sliwbl.com/login/'
user_email = "kiracase34"
user_password = "kiramira123"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

proxy_address = "45.130.254.133"
proxy_login = 'K0nENe'
proxy_password = 'uw7RQ3'
proxy_port = 8000

proxy_options = {
    "proxy":{
        "http":f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}",
        "https": f"http://{proxy_login}:{proxy_password}@{proxy_address}:{proxy_port}"
    }
}


def login(driver):
    driver.get(url)
    driver.maximize_window()

    try:
        driver.implicitly_wait(30)
        input_email = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/div/div/div/div/div/div/form/div[1]/div/dl[1]/dd/input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[5]/div/div/div/div/div/div/form/div[1]/div/dl[2]/dd/input')
        input_password.clear()
        input_password.send_keys(user_password)

        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'form > div.block-container > dl > dd > div > div.formSubmitRow-controls > button')
        sleep(1.5)
        driver.execute_script("arguments[0].click();", login_button)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")

    sleep(2)
    driver.get('https://s2.sliwbl.com/account/upgrades')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        actions = ActionChains(driver)
        login(driver)

        try:
            driver.implicitly_wait(20)
            choose_upgrade = driver.find_element(By.CSS_SELECTOR, 'div > ul > li:nth-child(1) > form > dl > dd > div.inputGroup > select')
            sleep(1.5)
            choose_upgrade.click()
            sleep(5)

            driver.implicitly_wait(5)
            for _ in range(3):
                actions.send_keys(Keys.ARROW_DOWN).perform()
                sleep(0.5)
            actions.send_keys(Keys.ENTER).perform()

            try:
                driver.implicitly_wait(10)
                submit = driver.find_element(By.CSS_SELECTOR, 'div > ul > li:nth-child(1) > form > dl > dd > div.inputGroup > button')
                sleep(1.5)
                driver.execute_script("arguments[0].click();", submit)

                driver.implicitly_wait(30)
                next_step_button = driver.find_element(By.CSS_SELECTOR, 'form > div > div > dl > dd > button > span')
                sleep(1.5)
                driver.execute_script("arguments[0].click();", next_step_button)
            except Exception as e:
                print(f"ERROR SUBMIT BUTTON \n{e}")
        except Exception as e:
            print(f"ERROR CHOOSE UPGRADE \n{e}")

        try:
            sleep(7.5)
            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR, 'div > div.wallet__content > ul > li:nth-child(2) > div').text

            driver.implicitly_wait(10)
            amount = driver.find_element(By.CSS_SELECTOR, 'div > div.wallet__content > ul > li.wallet__credential.tt > div').text.replace("USDT TRC20", '').replace(" ", '')

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


if __name__ == "__main__":
    wallet()