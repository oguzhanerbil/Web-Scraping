import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.emlakjet.com/satilik-konut/kocaeli/")

max_pages = 2
current_page = 1

while current_page <= max_pages:
    listings = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "_3qUI9q"))
    )
    for index in range(len(listings)):
        listings[index].click()
        fiyat_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "_2TxNQv"))
        )
        info_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//*[@id='bilgiler']/div/div[2]/div/div[1]/div[1]"))
        )
        for fiyat_element in fiyat_elements:
            print(fiyat_element.text)
        for info_element in info_elements:
            print(info_element.text)
        
        driver.back()
        


driver.close()
