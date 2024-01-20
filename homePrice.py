import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument(f'user-agent={"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.6099.225 Safari/537.36"}')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get("https://www.emlakjet.com/satilik-konut/bartin")
listings = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a._3qUI9q"))
)
tüm_sütunlar = ['Net Metrekare', 'Oda Sayısı', 'Bulunduğu Kat', 'Isıtma Tipi', 'Fiyat', 
                'Binanın Kat Sayısı', 'Kullanım Durumu',"Fiyat Durumu","Site İçerisinde","Kullanım Durumu","Kategorisi","Krediye Uygunluk","İpotek Durumu","Aidat","Banyo Sayısı"]
allCity = ["adana","adiyaman","afyonkarahisar","agri","aksaray","amasya","ankara","antalya","ardahan","artvin","aydin","balikesir","bartin","batman","bayburt","bilecik","bingöl","bitlis","bolu","burdur","bursa","canakkale","cankiri","corum","denizli","diyarbakir","düzce","edirne","elazig","erzincan","erzurum","eskisehir","gaziantep","giresun","gümüshane","hakkari","hatay","igdir","isparta","istanbul","izmir","kahramanmaras","karabük","karaman","kars","kastamonu","kayseri","kilis","kirikkale","kirklareli","kirşehir","kocaeli","konya","kütahya","malatya","manisa","mardin","mersin","mugla","mus","nevsehir","nigde","ordu","osmaniye","rize","sakarya","samsun","sanliurfa","siirt","sinop","sivas","sirnak","tekirdag","tokat","trabzon","tunceli","usak","van","yalova","yozgat","zonguldak"]
csv_dosya_adi = r"zingat3.csv"
data = pd.read_csv("zingat3.csv")
# Listeyi stringe çevirmek için
def listToString(s):
    str1 = " "
    return (str1.join(s)) 

while True:
    print("Merhaba babalık____________________________________________________________________________AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    for index in range(len(listings)):
        try:
            listings = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a._3qUI9q"))
            )
            print(len(listings))
            listings[index].click()
            fiyat_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "_2TxNQv"))
            )
            info_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//*[@id='bilgiler']/div/div[2]/div/div[1]/div[1]"))
            )
            detaylar = []
            fiyat = []
            
            for i in fiyat_elements:
                print(i.text)
                fiyat.append(i.text)
            for i in info_elements:
                print(i.text)
                detaylar.append(i.text)
            det_str = listToString(detaylar)
            ayri = det_str.split("\n")
            df = pd.DataFrame(ayri)
            print(df)
            df_yeni = df.iloc[6:53]
            #df_yeni.iloc[1] = df_yeni.iloc[1].str[0:3]
            df_yeni = df_yeni.reset_index()
            df_yeni.drop("index", axis = 1, inplace = True)
            df_liste = df_yeni.values.tolist()
            
            içerikler =[]
            headers = df_yeni.iloc[0::2].reset_index(drop=True)
            values = df_yeni.iloc[1::2].reset_index(drop=True)
            fiyat_sade = fiyat[1].strip()
            fiyat_sade = fiyat_sade.replace("TL","")
            
            # Oluşturulan DataFrame'i düzenleme
            düzenlenmiş_veri = pd.DataFrame(values).T
            düzenlenmiş_veri.columns = headers.values.flatten()
            düzenlenmiş_veri['Fiyat'] = fiyat_sade  # Fiyat sütunu ekleme
            
            # Tüm sütunlar için DataFrame oluştur
            # tam_veri = pd.DataFrame(columns=tüm_sütunlar)
            # tam_veri = tam_veri.add(düzenlenmiş_veri, ignore_index=True)
        
            
            
            # CSV dosyasının var olup olmadığını kontrol et
            if not os.path.exists(csv_dosya_adi):
                düzenlenmiş_veri.to_csv(csv_dosya_adi, encoding="utf-8", index=False, header=True, mode="w")
            else:
                düzenlenmiş_veri.to_csv(csv_dosya_adi, encoding="utf-8", index=False, header=False, mode="a")
            
                
            driver.back()
        except Exception as e:
            print(f"Hatalı kod: {e}")
    try:
        nextButton = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//*[@class='_3au2n_ OTUgAO']/div/a")))
        driver.execute_script("arguments[0].click();", nextButton)
        print("oh be oğluuuuuuuuuuum")
    except TimeoutException as e:
        print(f"Bir sorun oluştu: {e}")
        break

driver.close()
