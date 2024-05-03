from flask import jsonify
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# CONSTANS

url = 'https://bspin.io/ru/login'
user_email = "kiracase34@gmail.com"
user_password = "Kiramira123!"

# CHROME CONSTANS

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()
    api_key = paths[3].strip()
    ext = paths[1].strip()

# options.binary_location = chrome_path
options.add_extension(ext)

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
    driver.get(url)
    driver.maximize_window()
    actions = ActionChains(driver)

    handles = driver.window_handles
    print(handles)
    for handle in handles:
        driver.switch_to.window(handle)
        title = driver.title
        if "2Cap" in title:
            break

    try:
        input_data(driver, 30, '//input[@name="apiKey"]', api_key)
        click(driver, 30, '//*[@id="connect"]')
    except Exception as e:
        print(f'ERROR CONNECT API \n{e}')

    WebDriverWait(driver, 20).until(EC.alert_is_present())
    driver.switch_to.alert.accept()

    sleep(1.5)

    handles = driver.window_handles
    for handle in handles:
        driver.switch_to.window(handle)
        title = driver.title
        if ("коин" in title) or ("bspin" in title):
            break

    sleep(3.5)
    try:
        input_data(driver, 30, '//*[@id="content"]/div/div[2]/div[2]/div/form/div[1]/input', user_email)
        input_data(driver, 30, '//*[@id="content"]/div/div[2]/div[2]/div/form/div[2]/input', user_password)
    except Exception as e:
        print(f'ERROR LOGIN \n{e}')

    try:
        click(driver, 30, '//div[@class="captcha-solver captcha-solver_inner"]')
    except Exception as e:
        print(f'ERROR CLICK SOLVE CAPTCHA \n{e}')

    while True:
        try:
            driver.implicitly_wait(10)
            find_captcha_text = driver.find_element(By.XPATH, '//div[@class="captcha-solver-info"]')
            text = find_captcha_text.text
            if "шает" in text:
                sleep(5)
                print("Wait 5 seconds...")
            else:
                print("Solve")
                break
        except:
            print("Solve")
            break

    sleep(4.5)

    try:
        click(driver, 30, '//button[@class="xbtn large login-btn acc-btn login-page"]')
    except Exception as e:
        print(f'ERROR CLICK LOG BUT \n{e}')
        driver.implicitly_wait(20)
        find_input_tag = driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/div[2]/div/form/div[1]/input')
        if find_input_tag:
            return {"status": "0", "ext": "Login error. Check script."}
        else:
            print(f"ERROR DEPOS BUT \n{e}")

    try:
        sleep(5.5)
        click(driver, 30, '//*[@id="content"]/div[6]/div[1]/a')
        click(driver, 30, '//*[@id="user-action-buttons"]/a[2]')
    except Exception as e:
        print(f'ERROR CLICK \n{e}')

    try:
        click(driver, 30, '//*[@id="desktop-header-container"]/div/div/div/div[2]/div')
        sleep(1.5)
        click(driver, 30, '//*[@id="desktop-header-container"]/div/div/div/div[2]/div[2]/div[2]')
    except Exception as e:
        print(f'ERROR CLICK \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options, seleniumwire_options=proxy_options) as driver:
        log = login(driver)
        if log:
            return log

        sleep(4.5)
        try:
            driver.implicitly_wait(30)
            address_elem = driver.find_element(By.XPATH, '//*[@id="desktop-header-container"]/div/div/div/div[4]/button/div/span[2]')
            address = address_elem.text

            driver.implicitly_wait(30)
            amount_elem = driver.find_element(By.XPATH, '//*[@id="desktop-header-container"]/div/div/div/div[3]/div[1]/span')
            amount = amount_elem.text

            return {
                "address": address,
                "amount": amount.replace('Мин. депозит', '').replace("USDT", '').replace(" ", ''),
                "currency": "usdt"
            }
        except Exception as e:
            print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
