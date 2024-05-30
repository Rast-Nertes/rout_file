import selenium.webdriver.chrome.webdriver
from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# CONSTANS

url = 'https://s01.amerio.bet/en'
user_email = "+79872765544"
user_password = "AYQ2hr@eLut@dsY"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_argument('--log-level=3')
options.add_argument('--disable-remote-fonts')
options.add_experimental_option('prefs', {'intl.accept_languages': 'en, en_US'})

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    ext = paths[1].strip()

options.add_extension(ext)

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


def api_connect(driver):
    sleep(1.5)
    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        sleep(1.5)
        if "2Cap" in driver.title:
            break

    try:
        js_click(driver, 30, '//*[@id="autoSolveRecaptchaV2"]')
        js_click(driver, 30, '//*[@id="autoSolveInvisibleRecaptchaV2"]')
        js_click(driver, 30, '//*[@id="autoSolveRecaptchaV3"]')
        js_click(driver, 30, '//*[@id="autoSolveHCaptcha"]')

        input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        click(driver, 30, '//*[@id="connect"]')
        sleep(4.5)
        driver.switch_to.alert.accept()
    except Exception as e:
        print(f'ERROR CLICK \n{e}')

    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        sleep(1.5)
        if not("2Cap" in driver.title):
            break


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
    api_connect(driver)
    driver.get(url)

    try:
        click(driver, 30, '//*[@id="__nuxt"]/div/div/div/header/div[1]/div/div[3]/div/button[2]')
        input_data(driver, 30, '//input[@type="email"]', user_email)
        input_data(driver, 30, '//input[@type="password"]', user_password)
        click(driver, 30, '//*[@id="__nuxt"]/div/div/div/header/div[3]/div/div/div[2]/div/div[3]/div[2]/button')
    except Exception as e:
        return {"status": "0", "ext": f"error login \n{e}"}

    try:
        sleep(4.5)
        js_click(driver, 30, '//div[@class="popup-top-cross"]')
        click(driver, 30, '//*[@id="__nuxt"]/div/div/div/header/div[1]/div/div[4]/div/div[2]/div[1]/button')
        js_click(driver, 30, "//div[contains(@class, 'deposit-wallet-name') and text()='USDT TRC-20']")
    except Exception as e:
        input("press")
        return {"status": "0", "ext": f"error depos trc20 \n{e}"}

    try:
        sleep(5)
        input_data(driver, 5, '//*[@id="__nuxt"]/div/div/div/header/div[3]/div/div[2]/div/div[2]/div[1]/div[2]/div[2]/input', '5')
    except:
        pass

    try:
        click(driver, 30, '//*[@id="__nuxt"]/div/div/div/header/div[3]/div/div[2]/div/div[2]/div[4]/button')
    except Exception as e:
        input("prs")
        return {"status": "0", "ext": f"error click depos but \n{e}"}


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//*[@id="__nuxt"]/div/div/div/header/div[3]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div[2]/div/span')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="__nuxt"]/div/div/div/header/div[3]/div/div[2]/div[2]/div/div/div[2]/div/div/div/div[3]/div/div[2]/div/span')
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
