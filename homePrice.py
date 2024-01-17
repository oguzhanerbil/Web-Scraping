import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

# Web sürücüsünü yükleyin
driver = webdriver.Chrome()

driver.get("https://www.emlakjet.com/satilik-konut/kocaeli/")
i = 1
while i <= 2:
    classAdress = driver.find_element(By.XPATH,"//*[@id='listing-search-wrapper']")
    classes = driver.find_elements(By.CLASS_NAME,"_3qUI9q")
    for tikla in classes:
        sleep(5)
        tikla.click()
        elements = driver.find_elements(By.XPATH,"//*[@id='bilgiler']/div/div[2]/div/div[1]/div[1]")
        fiyat = driver.find_elements(By.CLASS_NAME,"_2TxNQv")
        detaylar = []
        for i in fiyat:
            fiyat = i.text
        print("LAAAN"+fiyat)
        for i in elements:
            print(i.text)
            detaylar.append(i.text)
        driver.execute_script("window.history.go(-1)")




driver.close()
