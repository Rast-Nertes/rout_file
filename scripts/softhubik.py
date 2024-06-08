from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By

# CONSTANS

url = 'https://softhubik.ru/cs2.html'
user_email = "yewoxo4550@otemdi.com"
user_password = "onvB2mkVH5c"

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

    try:
        driver.implicitly_wait(20)
        a_href = driver.find_element(By.XPATH, '//*[@id="u6068-6"]').get_attribute('href')
        driver.get(a_href)
    except Exception as e:
        return {"status":"0", "ext":f"error href {e}"}

    try:
        click(driver, 20, '//*[@id="btn_next"]')
    except Exception as e:
        return {"status":"0", "ext":f"error next but {e}"}

    try:
        driver.implicitly_wait(30)
        click_select = driver.find_element(By.XPATH, '//*[@id="TypeCurr_msdd"]')
        sleep(1.5)
        click_select.click()

        driver.implicitly_wait(20)
        choose_tc20 = driver.find_element(By.XPATH, '//span[@class="ddlabel" and text()="USDT"]')
        sleep(1.5)
        choose_tc20.click()
        sleep(2.5)
    except Exception as e:
        return {"status":"0", "ext":f"error choose usdt {e}"}

    try:
        input_data(driver, 20, '//*[@id="email"]', user_email)
        sleep(1)
        input_data(driver, 20, '//*[@id="Re_Enter_Email"]', user_email)
        sleep(1)
        click(driver, 20, '//*[@id="pay_btn"]')
    except Exception as e:
        return {"status":"0", "ext":f"error submit  {e}"}


def get_wallet():
    with webdriver.Chrome(options=options) as driver:
        login(driver)

        try:
            sleep(3.5)
            driver.implicitly_wait(40)
            amount = driver.find_element(By.XPATH, '//*[@id="form1"]/section/section/div[2]/div[2]/div[4]/p/span').text.replace("USDT", '').replace(" ", '')

            driver.implicitly_wait(10)
            address = driver.find_element(By.XPATH, '//*[@id="form1"]/section/section/div[2]/div[2]/div[4]/div/div[1]/div/span').text

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
