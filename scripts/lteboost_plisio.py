from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent
from flask import jsonify
from undetected_chromedriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = ChromeOptions()
chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0')
chrome_options.headless = False
user_agent = UserAgent()
chrome_options.add_argument(f"user-agent={user_agent.random}")

url = 'https://lteboost.com'

user_login = 'kiracase34@gmail.com'
user_password = 'kiramira000'


def login(driver):
    try:
        driver.get(url)
        driver.maximize_window()
        element_start = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="body"]/div[1]/header/div[1]/div[2]/div/ul[2]/li[2]/a/span[2]'))
        )
        element_start.click()
        driver.find_element(By.ID, 'email').send_keys(user_login)
        sleep(1)
        driver.find_element(By.ID, 'password').send_keys(user_password)
        sleep(1)
        driver.find_element(By.XPATH, '/html/body/div/div[2]/div/form/div[5]/button').click()
        sleep(1)
    except Exception as e:
        print(f"ERROR1 -- {e}")


def get_wallet():
    with webdriver.Chrome() as driver:
        login(driver)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="main-menu"]/li[7]/a'))
            )
            element.click()

            sleep(1)
            driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/p/a[2]').click()
            sleep(3)
            arrows = driver.find_element(By.XPATH, '//*[@id="paymethod"]')
            arrows.click()
            arrows.send_keys(Keys.ARROW_DOWN)#1
            sleep(1)
            arrows.send_keys(Keys.ARROW_DOWN)#2
            sleep(1)
            arrows.send_keys(Keys.ARROW_DOWN)#3
            sleep(1)
            arrows.send_keys(Keys.ARROW_DOWN)  # 4

            money_input = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/div/div/div[2]/div[2]/div/input'))
            )
            money_input.send_keys('1000')

            money_input_accept = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div[2]/div[3]/div/div/div[2]/div[3]/button'))
            )
            money_input_accept.click()

            # input("press")

            try:
                driver.implicitly_wait(5)
                click_check_pay = driver.find_element(By.XPATH, "//button[@class='btn btn-danger btn-sm btn-block checkpaybtn']")
                sleep(1.5)
                driver.execute_script("arguments[0].click();", click_check_pay)
            except:
                print("error accept")
                # return {"status":"0", "ext":"Accept button error"}

            # email_input = WebDriverWait(driver, 10).until(
            #     EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div[2]/form/div[2]/div/div[2]/input'))
            # )
            # email_input.send_keys(user_login)
            #
            # email_input_accept = WebDriverWait(driver, 10).until(
            #     EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[2]/form/div[2]/button'))
            # )
            # email_input_accept.click()

            # driver.execute_script("window.scrollBy(0, 500);")

            wallet_chouse = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//img[@alt="Tether"]'))
            )
            wallet_chouse.click()

            wallet_chouse_accept = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[3]/div[2]/button/div'))
            )
            wallet_chouse_accept.click()

            id_wallet = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[7]'))
            )
            id_wallet = id_wallet.text

            min_value = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[6]/div/span/strong[1]'))
            )
            min_value = min_value.text


            return {
                "adress":id_wallet,
                "amount":min_value,
                "currency":"usdt"
            }

        except Exception as e:
            print(f"ERROR3 -- {e}")


def wallet():
    wallet_data = get_wallet()
    print(wallet_data)
    return jsonify(wallet_data)
