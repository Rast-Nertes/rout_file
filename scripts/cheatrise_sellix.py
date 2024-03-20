from flask import jsonify
from selenium_driverless.sync import webdriver
from selenium_driverless.types.by import By
from time import sleep
from fake_useragent import UserAgent


# CONSTANS

url = 'https://cheatrise.com/games/eft/spoofer'
user_email = "alex37347818@gmail.com"
user_password = "onvB2mkVH5c"

# CHROME CONSTANS

with open('config.txt') as file:
    paths = file.readlines()
    chrome_path = paths[0].strip()

options = webdriver.ChromeOptions()
user_agent = UserAgent()
options.add_argument(f"user-agent={user_agent.random}")
options.add_argument("--disable-save-password-bubble")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-extensions")
options.add_argument("--no-sandbox")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.binary_location = chrome_path


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        driver.maximize_window()
        driver.get(url)

        try:
            buy_button = driver.find_element(By.CSS_SELECTOR, 'div.list.row > div.prices-block.col-md-4 > div > button', timeout=40)
            sleep(1.5)
            driver.execute_script("arguments[0].click();", buy_button)
        except Exception as e:
            print(f"ERROR BUY BUTTON \n{e}")

        try:
            input_email = driver.find_element(By.ID, 'purchases-email', timeout=30)
            input_email.write(user_email)

            choose_freekassa = driver.find_element(By.CSS_SELECTOR, 'div.pay-sellix.linear-gradient-border.purple', timeout=20)
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_freekassa)
        except Exception as e:
            print(f"ERROR CHOOSE PAYMENT \n{e}")

        try:
            sleep(5)
            find_frame = driver.find_elements(By.TAG_NAME, 'iframe')
            sleep(2)
            iframe_document = find_frame[0].content_document

            checkbox = iframe_document.find_element(By.XPATH,
                                                          '//label[@class="ctp-checkbox-label"]/input', timeout=20)
            sleep(3)
            checkbox.click()
        except Exception as e:
            print(f"CLICK \n{e}")

        try:
            choose_tether = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[2]/div[1]/div[3]/div[2]', timeout=30)
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_tether)

            choose_trc20 = driver.find_element(By.XPATH, '//*[@id="gateway-body"]/div[2]/div[1]/div[3]/div[2]/div[2]/div[3]', timeout=20)
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_trc20)

            submit_payment = driver.find_element(By.XPATH, '//*[@id="gateway-footer"]/div/button', timeout=10)
            sleep(1.5)
            driver.execute_script("arguments[0].click();", submit_payment)
        except Exception as e:
            print(f"ERROR CHOOSE TRC20 \n{e}")

        try:
            show_details_button = driver.find_element(By.XPATH, '//*[@id="embed-body"]/div/div[1]/div[6]/div[2]/div[1]', timeout=20)
            sleep(1.5)
            driver.execute_script("arguments[0].click();", show_details_button)
        except Exception as e:
            print(f"SHOW DETAILS ERROR \n{e}")

        try:
            address = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[6]/div[2]/div[2]/div/div[2]/span[2]/div/div[2]/span', timeout=20).text

            amount = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[6]/div[2]/div[2]/div/div[2]/span[1]/div/div[2]/span', timeout=20).text

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
