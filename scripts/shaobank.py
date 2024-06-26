from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


# CONSTANS

url = 'https://shaobank.com/auth/signin'
user_email = "alex37347818@gmail.com"
user_password = "azPid@n#4zPJLsN"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")


##PROXY_CONSTANS

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
    driver.maximize_window()
    driver.get(url)

    try:
        driver.implicitly_wait(30)
        sleep(2)
        input_email = driver.find_element(By.XPATH, '/html/body/app-root/ng-component/div/section/div/div/div[1]/ng-component/form/fieldset/div[2]/div[1]/label/input')
        input_email.clear()
        input_email.send_keys(user_email)

        driver.implicitly_wait(10)
        input_password = driver.find_element(By.XPATH, '/html/body/app-root/ng-component/div/section/div/div/div[1]/ng-component/form/fieldset/div[2]/div[2]/label/input')
        input_password.clear()
        input_password.send_keys(user_password)


        driver.implicitly_wait(10)
        login_button = driver.find_element(By.CSS_SELECTOR, 'section > div > div > div.col-lg-8 > ng-component > form > fieldset > button')
        sleep(3)
        driver.execute_script("arguments[0].click();", login_button)
        #Время залогиниться
        sleep(7.5)
    except Exception as e:
        print(f"LOGIN ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        actions = ActionChains(driver)
        login(driver)

        sleep(2)
        driver.get('https://shaobank.com/account/bonds')

        try:
            driver.implicitly_wait(10)
            close = driver.find_element(By.CSS_SELECTOR, 'body > app-root > ng-component:nth-child(5) > div > div > div.cab-modal__close')
            driver.execute_script("arguments[0].click();", close)
        except:
            pass

        try:
            driver.implicitly_wait(10)
            sleep(3)
            choose_selection = driver.find_element(By.CSS_SELECTOR, 'ng-component > account-bond-form > form > div.cab-box__row > div:nth-child(1) > div.cab-input.sel > div > div > div.jq-selectbox__select > div.jq-selectbox__trigger')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_selection)
        except Exception as e:
            print(f"ERROR CHOOSE \n{e}")

        for _ in range(4):
            actions.send_keys(Keys.ARROW_DOWN).perform()
            sleep(0.5)
        actions.send_keys(Keys.ENTER).perform()
        sleep(0.5)

        try:
            driver.implicitly_wait(10)
            next_step_button = driver.find_element(By.CSS_SELECTOR, 'div.col-lg-6 > div > ng-component > account-bond-form > form > button')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", next_step_button)
        except Exception as e:
            print(f'NEXT STEP ERROR \n{e}')

        try:
            sleep(4)
            driver.implicitly_wait(10)
            address = driver.find_element(By.CSS_SELECTOR, 'ng-component:nth-child(5) > div > div > div.cab-modal__box > div:nth-child(5) > span').text

            driver.implicitly_wait(10)
            amount = driver.find_element(By.CSS_SELECTOR, 'ng-component:nth-child(5) > div > div > div.cab-modal__box > div:nth-child(3) > span').text.replace('USDT TRC20', "").replace(" ", '')

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
