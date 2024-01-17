from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
print("haa")
class DataFetch:
    def __init__(self):
        options = webdriver.ChromeOptions()
        service = Service(executable_path=r'C:\webdriver\chromedriver.exe')
        self.browser = webdriver.Chrome(options=options,service=service)
    def fetch(self):
        self.browser.get("https://www.emlakjet.com/satilik-konut/kocaeli/")
        
        element = WebDriverWait(self.browser, 1).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='searchResultsTable']/tbody/tr[1]/td[4]"))
        )
        print(element.text)  # Print the element's text
        
        
DataFetch().fetch()
sleep(100)