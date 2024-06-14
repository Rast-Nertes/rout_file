from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from flask import Flask, jsonify
from selenium import webdriver
from time import sleep

USERNAME = "kiracase34@gmail.com" # username
PASSWORD = "kiraadpro9" # password


def captcha_and_login(driver):
    url = "https://advertiser.adprofex.com/login"
    driver.maximize_window()
    driver.get(url); driver.implicitly_wait(30)
    try:
        input_email = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div/form/div[1]/div[1]/label/div/div[1]/div/input'))
        )
        input_email.send_keys(USERNAME)

        input_password = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div/form/div[1]/div[2]/label/div/div[1]/div[1]/input'))
        )
        input_password.send_keys(PASSWORD)
    except Exception as e:
        print(f"INPUT ERROR \n{e}")

    try:
        click_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="q-app"]/div/div[2]/div[2]/div/div/form/div[2]/div/button'))
        )
        click_button.click()
    except Exception as e:
        print(f"CLICK ERROR \n{e}")


def get_wallet():
    with webdriver.Chrome() as driver:
        captcha_and_login(driver)
        sleep(5)
        driver.get('https://advertiser.adprofex.com/lk/balance')

        try:

            add_funds = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="q-app"]/div/div[4]/main/div/div/div/div[2]/button'))
            )
            add_funds.click()
        except Exception as e:
            print(f"ADD FUNDS ERROR \n{e}")
            driver.implicitly_wait(10)
            find_input_tag = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div[2]/div/div/form/div[1]/div[1]/label/div/div[1]/div/input',)
            if find_input_tag:
                return {"status": "0", "ext": "Login error. Check script."}
            else:
                print(f"ERROR DEPOS BUT \n{e}")

        try:
            driver.implicitly_wait(10)
            click_other_amount = driver.find_element(By.XPATH, '//*[@id="q-app"]/div/div[4]/main/div/div/div/div[2]/div[1]/div/div/div[6]/div[2]/div[2]')
            click_other_amount.click()
        except Exception as e:
            print(f'ERROR CHOOSE OTHER AMOUNT \n{e}')

        try:
            choose_capitalist_method = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="q-app"]/div/div[4]/main/div/div/div/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/div[1]'))
            )
            sleep(2.5)
            choose_capitalist_method.click()
            # driver.execute_script("arguments[0].click();", choose_capitalist_method)
        except Exception as e:
            print(f"CHOOSE ERROR \n{e}")

        try:
            ticket = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="q-app"]/div/div[4]/main/div/div/div/div[2]/div[3]/label/div/div[1]/div'))
            )
            ticket.click()

            add_funds_button = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="q-app"]/div/div[4]/main/div/div/div/div[2]/div[4]/button[2]'))
            )
            add_funds_button.click()
        except Exception as e:
            print(f"TICKET CHOOSE ERROR \n{e}")

        sleep(3.5)
        windows = driver.window_handles
        for window in windows:
            driver.switch_to.window(window)
            tittle = driver.title
            print(tittle)
            sleep(1)
            if not("ex" in tittle):
                break

        driver.implicitly_wait(90)
        address = driver.find_element(By.XPATH, '//*[@id="order-page"]/div[4]/div/div/div[3]/div[2]/div[2]/div[2]/button').get_attribute('data-clipboard-text')

        driver.implicitly_wait(30)
        amount = driver.find_element(By.XPATH, '//*[@id="order-page"]/div[4]/div/div/div[3]/div[2]/p/strong').text.replace("USDT (TRC20)", "").replace(" ", "")

        return {
            "address": address,
            "amount": amount,
            "currency": "usdt"
        }


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
