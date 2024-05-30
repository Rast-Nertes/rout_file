from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'http://mydirtyhobby.com/'
user_email = "rwork"
user_password = "00001111Rw!"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
options.add_argument("--disable-save-password-bubble")
options.add_argument('--log-level=3')
options.add_argument('--disable-remote-fonts')
options.add_experimental_option('prefs', {'intl.accept_languages': 'en, en_US'})

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    ext = paths[1].strip()

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


def wait_visibility(driver, time, XPATH):
    WebDriverWait(driver, time).until(
        EC.visibility_of_element_located((By.XPATH, XPATH))
    )
    sleep(2.5)


def click(driver, time, XPATH):
    driver.implicitly_wait(time)
    elem_click = driver.find_element(By.XPATH, XPATH)
    sleep(1.5)
    elem_click.click()


def js_click(driver, time, XPATH):
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
    driver.maximize_window()
    driver.get(url)

    try:
        wait_visibility(driver, 30, '//button[@class="en enter-btn mdh"]')
        click(driver, 10, '//button[@class="en enter-btn mdh"]')
    except:
        pass

    try:
        wait_visibility(driver, 30, '//*[@id="qa_head_login_btn"]')
        click(driver, 10, '//*[@id="qa_head_login_btn"]')
    except Exception as e:
        print(f'ERROR PATH TO LOGIN \n{e}')

    try:
        wait_visibility(driver, 30, '//*[@id="qa_popup_login_input"]')
        input_data(driver, 10, '//*[@id="qa_popup_login_input"]', user_email)
        input_data(driver, 10, '//*[@id="qa_popup_login_pass"]', user_password)
    except Exception as e:
        print(f'ERROR INPUT LOG DATA \n{e}')

    try:
        wait_visibility(driver, 30, '//*[@id="qa_popup_login_submit"]')
        click(driver, 10, '//*[@id="qa_popup_login_submit"]')
    except Exception as e:
        print(f'ERROR log')

    try:
        wait_visibility(driver, 30, '(//*[@id="qa_coins_jp_method_epayment_Crypto"])[2]')
        click(driver, 10 ,'(//*[@id="qa_coins_jp_method_epayment_Crypto"])[2]')
        sleep(1.5)
        click(driver, 10, '(//*[@id="qa_coins_jp_amnt_850"])[2]')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')

    try:
        wait_visibility(driver, 30, '//*[@id="qa_coins_jp_submit"]')
        click(driver, 10, '//*[@id="qa_coins_jp_submit"]')
    except Exception as e:
        print(f'ERROR SUBMIT \n{e}')

    sleep(5)
    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        sleep(1.5)
        if not("ents" in driver.title):
            break

    try:
        wait_visibility(driver, 30, '//div[@data-icon="USDT_TRX"]')
        js_click(driver, 10, '//div[@data-icon="USDT_TRX"]')
    except Exception as e:
        print(f'ERROR CHOOSE TRC20 \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//*[@id="root"]/div[1]/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div[1]')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//div[@class="inner-price"]')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace("USDT", '').replace("(5 USD)", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)