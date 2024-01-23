import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import sys
from time import sleep
def start_browser():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument("--headless")
    options.add_argument(f'user-agent={"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.6099.225 Safari/537.36"}')
    driver = webdriver.Chrome(options=options)
    return driver

tüm_sütunlar = ['Net Metrekare',"Brüt Metrekare", 'Oda Sayısı', 'Bulunduğu Kat',"Eşya Durumu","Binanın Yaşı", 'Isıtma Tipi', 'Fiyat', "Şehir",
                'Binanın Kat Sayısı', 'Kullanım Durumu',"Fiyat Durumu","Yatırıma Uygunluk","İlan Güncelleme Tarihi","Site İçerisinde","Takas","İlan Oluşturma Tarihi","Türü",
                "Kullanım Durumu","Kategorisi","Krediye Uygunluk","Tapu Durumu","İpotek Durumu","Aidat","İlan Numarası","Banyo Sayısı"]
allCity = ["adana","adiyaman","afyonkarahisar","agri","aksaray","amasya","ankara","antalya","ardahan","artvin","aydin","balikesir","bartin","batman","bayburt","bilecik","bingol","bitlis","bolu","burdur","bursa","canakkale","cankiri"
           ,"corum","denizli","diyarbakir","duzce","edirne","elazig","erzincan","erzurum","eskisehir","gaziantep",
           "giresun","gumushane","hakkari","hatay","igdir","isparta","istanbul","izmir","kahramanmaras",
           "karabuk","karaman","kars","kastamonu","kayseri","kilis","kirikkale","kirklareli","kirsehir","kocaeli",
           "konya","kutahya","malatya","manisa","mardin","mersin","mugla","mus","nevsehir","nigde","ordu","osmaniye",
           "rize","sakarya","samsun","sanliurfa","siirt","sinop","sivas","sirnak","tekirdag","tokat","trabzon","tunceli","usak","van","yalova","yozgat","zonguldak"]

csv_dosya_adi = r"AllData.csv"
toplu_veriler = pd.DataFrame(columns=tüm_sütunlar)
# Listeyi stringe çevirmek için
def listToString(s):
    str1 = " "
    return (str1.join(s)) 
k = 0
c = 0
sayfaSayac = 0
for sehir in allCity:
    while True:
        sayfaSayac+=1
        driver = start_browser()
        driver.get(f"https://www.emlakjet.com/satilik-konut/{sehir}/{sayfaSayac}")
        sleep(3)
        listings = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a._3qUI9q"))
        )
        sleep(1)
        for index in range(len(listings)):
            try:
                listings = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a._3qUI9q"))
                )
                listings[index].click()
                fiyat_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "_2TxNQv"))
                )
                moreSee = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,"XoBBT3")))
                driver.execute_script("arguments[0].click();", moreSee)
                info_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "_2HQCBI"))
                )
                detaylar = []
                fiyat = []
                for i in fiyat_elements:
                    fiyat.append(i.text)
                for i in info_elements:
                    detaylar.append(i.text)
                k+=1
                print(k)
                detaylar.insert(1, "\n")
                det_str = listToString(detaylar)
                ayri = det_str.split("\n")
                df = pd.DataFrame(ayri)
                df_yeni = df.iloc[:]
                # df_yeni.iloc[1] = df_yeni.iloc[1].str[0:3]
                df_yeni = df_yeni.reset_index()
                df_yeni.drop("index", axis = 1, inplace = True)
                df_liste = df_yeni.values.tolist()
                içerikler =[]
                headers = df_yeni.iloc[0::2].reset_index(drop=True)
                values = df_yeni.iloc[1::2].reset_index(drop=True)
                fiyat_sade = fiyat[1].strip()
                fiyat_sade = fiyat_sade.replace("TL","")
                düzenlenmiş_veri = pd.DataFrame([values.values.flatten()], columns=headers.values.flatten())
                düzenlenmiş_veri = düzenlenmiş_veri.reindex(columns=tüm_sütunlar)  # Eksik sütunları NaN ile doldur
                düzenlenmiş_veri['Fiyat'] = fiyat_sade  # Fiyat sütunu ekleme
                düzenlenmiş_veri["Şehir"] = sehir
                toplu_veriler = pd.concat([toplu_veriler, düzenlenmiş_veri], ignore_index=True)
                    
                driver.back()
            except Exception as e:
                print(f"Hatalı kod: {e}, Satır: {sys.exc_info()[-1].tb_lineno}")
        try:
            driver.quit()
         
            c+=1
            print(c)
        except TimeoutException as e:
            sayfaSayac = 0
            print(f"Bir sorun oluştu: {e}")
            break
        
if not os.path.exists(csv_dosya_adi):
    toplu_veriler.to_csv(csv_dosya_adi, encoding="utf-8", index=False, header=True, mode="w")
else:
    toplu_veriler.to_csv(csv_dosya_adi, encoding="utf-8", index=False, header=False, mode="a")
driver.close()
