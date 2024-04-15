from flask import jsonify
from selenium import webdriver
from time import sleep
import pyautogui
from twocaptcha import TwoCaptcha
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://nudeitnow.com/auth/login'
user_email = "rwork875@gmail.com"
user_password = "718930L21"
site_key = '6LfBfjIpAAAAAORmdXbLeyY74J1zS11nBBYPCqCt'

# CHROME CONSTANS

#718930L21

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")

with open('C:/Users/Acer/Desktop/py_scripts/result/ROUT_FILE/config.txt') as file:
    paths = file.readlines()
    ext = paths[1].strip()
    api_key = paths[3].strip()

options.add_extension(ext)


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

    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        print(driver.title)
        sleep(1.5)
        if "2Cap" in driver.title:
            break

    try:
        input_data(driver, 30, '/html/body/div/div[1]/table/tbody/tr[1]/td[2]/input', api_key)
        sleep(1)
        click(driver, 20, '//*[@id="connect"]')
    except Exception as e:
        print(f'ERROR CAP CONNECT\n{e}')

    sleep(4.5)
    pyautogui.press('enter')

    windows = driver.window_handles
    for win in windows:
        sleep(1.5)
        driver.switch_to.window(win)
        if not("2Cap" in driver.title):
            break

    try:
        input_data(driver, 30, '//*[@id="email"]', user_email)
        sleep(1)
        input_data(driver, 30, '//*[@id="password"]', user_password)
    except Exception as e:
        print(f'ERROR INPUT DATA \n{e}')

    try:
        click(driver, 20, '/html/body/div[2]/div/div/div/div/div/div[5]/div/div/div/div[2]/div[2]')
    except Exception as e:
        print(f'ERROR SOLVE CAPTCHA \n{e}')

    while True:
        try:
            driver.implicitly_wait(10)
            find_text_captha = driver.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div/div/div[5]/div/div/div/div[2]/div[2]').text
            sleep(2.5)
            if "Решается" in find_text_captha:
                sleep(3.5)
                print('Wait 5 sec...')
            else:
                print('Solve!')
                sleep(1.5)
                break
        except:
            break


    try:
        click(driver, 20, '//*[@id=":r2:"]')
    except Exception as e:
        print(f'ERROR LOG BUT \n{e}')

    sleep(3.5)
    driver.get('https://nudeitnow.com/billing')

    try:
        click(driver, 20, '/html/body/div[2]/div/div/div[5]/div[1]/div/div')
        sleep(2.5)

        click(driver, 20, '/html/body/div[2]/div/div/div[6]/div/div/div/div[4]/div[1]/button')
        sleep(3.5)
    except Exception as e:
        print(f'ERROR CHOOSE TARIFF \n{e}')

    windows = driver.window_handles
    for win in windows:
        driver.switch_to.window(win)
        print(driver.title)
        sleep(1.5)
        if "rypto" in driver.title:
            break

    try:
        # sleep(3.5)
        # driver.refresh()

        click(driver, 20, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[3]/button')
    except Exception as e:
        print(f'ERROR NEXT BUT \n{e}')


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(2.5)
            driver.implicitly_wait(25)
            amount = driver.find_element(By.XPATH,
                                         '//*[@id="app"]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/span').text.replace(
                "USDT", '').replace(" ", '')

            driver.implicitly_wait(20)
            address = driver.find_element(By.XPATH,
                                          '//*[@id="app"]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div/span').text

            return {
                "address": address,
                "amount": amount,
                "currency": "usdt"
            }
        except Exception as e:

            try:
                click(driver, 20, '//*[@id="app"]/div/div/div/div[2]/div[2]/div[1]/div[3]/button')
            except Exception as e:
                print(f'ERROR NEXT BUT \n{e}')

            try:
                    sleep(2.5)
                    driver.implicitly_wait(65)
                    amount = driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[1]/div[2]/span').text.replace("USDT", '').replace(" ", '')

                    driver.implicitly_wait(20)
                    address = driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div[2]/div/div[2]/div[1]/div/span').text

                    return {
                        "address": address,
                        "amount": amount,
                        "currency": "usdt"
                    }
            except Exception as e:
                print(f"ERROR DATA \n{e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
