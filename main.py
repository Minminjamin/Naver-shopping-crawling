import time
import requests
from time import sleep
import re, requests, csv
from bs4 import BeautifulSoup as bs
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

keys = Keys()

#https://blog.naver.com/yk02061/223047318794

url = "https://brand.naver.com/skinfood/products/7926935977" 

# 크롬 드라이버 최신 버전 설정
service = ChromeService(executable_path=ChromeDriverManager().install())
options = ChromeOptions()

# chrome driver
driver = webdriver.Chrome(service=service, options=options) # <- options로 변경

# 브라우저 꺼짐 방지
chrome_options = ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러 메세지 없애기
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) 



# driver = webdriver.Chrome(executable_path='/Use
# rs/user/.ipython/chromedriver.exe')
driver.get(url)

page = requests.get("https://brand.naver.com/skinfood/products/7926935977")

from selenium import webdriver 
count = 0
stop = int(input("전체 리뷰 수를 입력해주세요 "))/11
next_btn = ['a:nth-child(2)', 'a:nth-child(3)', 'a:nth-child(4)', 'a:nth-child(5)', 'a:nth-child(6)', 'a:nth-child(7)',
        'a:nth-child(8)', 'a:nth-child(9)', 'a:nth-child(10)', 'a:nth-child(11)', 'a.fAUKm1ewwo._2Ar8-aEUTq']
review_list = []

driver.implicitly_wait(10)

while count < stop:
    for pagenum in next_btn:
        driver.find_element('#QNA > div > div.bd_3WYRt.bd_xW-5i.bd_39eTe._nlog_impression_element > a:nth-child(1)').click()
       
        # driver.find_element('#REVIEW > div > div._180GG7_7yx > div.cv6id6JEkg > div > div >'+str(pagenum)+'').click()

        time.sleep(2)
        for i in range(0,20):
            html = driver.page_source
            soup = bs(html, "html.parser")
            review = soup.find_all('div',class_='_19SE1Dnqkf')
            review = review[i].text
            review = re.sub('[^#0-9a-zA-Zㄱ-ㅣ가-힣 ]',"",review)
            review_list.append(review)
    count = count + 1


# review_list
    
df = pd.DataFrame({"리뷰":review_list})
df.to_csv("c:/Users/user/review scrap/스킨푸드 도토리패드.csv", encoding='cp949')
print("저장 완료되었습니다.")