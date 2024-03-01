from flask import jsonify
from selenium import webdriver
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#CONSTANS

url = 'https://noveltydocumentstore.ws/'
user_login = "kiracase34@gmail.com"
user_password = "kiramira555"

#CHROME CONSTANS

#####

def get_wallet():
    with webdriver.Chrome() as driver:
        driver.get(url)
        driver.maximize_window()
        
        sleep(10)
        
        driver.get(url)

        try:
            driver.implicitly_wait(10)
            choose_license = driver.find_element(By.CSS_SELECTOR, 'div.woocommerce.columns-5 > ul > li.product.type-product.post-1104.status-publish.first.instock.product_cat-dl.product_cat-united-kingdom.product_tag-dl.product_tag-uk.has-post-thumbnail.sale.downloadable.virtual.purchasable.product-type-simple > a > h2')
            sleep(1.5)
            driver.execute_script("arguments[0].click();", choose_license)
        except Exception as e:
            print(f"CHOOSE LICENSE ERROR \n{e}")

        try:
            driver.implicitly_wait(20)
            amount = driver.find_element(By.XPATH, '//*[@id="product-1104"]/div[1]/div[2]/p[1]/span/ins/span/bdi').text.replace("$", "")

            driver.implicitly_wait(20)
            address = driver.find_element(By.XPATH, '//*[@id="tab-description"]/div[2]/table/tbody[1]/tr[4]/td[2]').text

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
