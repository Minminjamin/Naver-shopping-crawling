# https://velog.io/@onicle/%ED%81%AC%EB%A1%A4%EB%A7%81%EB%84%A4%EC%9D%B4%EB%B2%84-%EC%8A%A4%EB%A7%88%ED%8A%B8%EC%8A%A4%ED%86%A0%EC%96%B4-%EB%A6%AC%EB%B7%B0-%EC%88%98%EC%A7%91

import re
from bs4 import BeautifulSoup
 
import pandas as pd
from datetime import datetime
import time
 
# selenium import
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions() # 크롬 옵션 객체 생성
# options.add_argument('headless') # headless 모드 설정 -> 해당 옵션 적용 시 PDF 다운 불가
options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument('--no-sandbox') 

service = Service(executable_path=ChromeDriverManager().install())

url : str = input('리뷰를 수집할 주소를 입력 : ')
driver = webdriver.Chrome(service = service, options=options)
# wait seconds...
driver.implicitly_wait(3)



driver.get(url)
time.sleep(3)

driver.find_element(By.CSS_SELECTOR,'#content > div > div.z7cS6-TO7X > div._27jmWaPaKy > ul > li:nth-child(2) > a').click()
time.sleep(3)

# 최신순 버튼 클릭
driver.find_element(By.CSS_SELECTOR,'#REVIEW > div > div._2LvIMaBiIO > div._2LAwVxx1Sd > div._1txuie7UTH > ul > li:nth-child(2) > a').click()

time.sleep(3)
# 1. 셀레니움으로 html가져오기
html_source = driver.page_source
# 2. bs4로 html 파싱
soup = BeautifulSoup(html_source, 'html.parser')
time.sleep(0.5)

# 3. 리뷰 정보 가져오기
reviews = soup.findAll('li', {'class': 'BnwL_cs1av'})

#사용할 list 최상단 선언
write_dt_lst = []
item_nm_lst = []
content_lst = []

# 4. 한페이지 내에서 수집 가능한 리뷰 리스트에 저장
for review in range(len(reviews)):
    
    # 4-1.리뷰작성일자 수집
    write_dt_raw = reviews[review].findAll('span' ,{'class' : '_2L3vDiadT9'})[0].get_text()
    write_dt = datetime.strptime(write_dt_raw, '%y.%m.%d.').strftime('%Y%m%d')
    
    # 4-2.상품명 수집
    # 4-2-(1) 상품명이 포함된 css 선택자 입력 
    item_nm_info_raw = reviews[review].findAll('div', {'class' : '_2FXNMst_ak'})[0].get_text()
    item_nm_info_for_del = ''

    try:
        item_nm_info_for_del = reviews[review].findAll('div', {'class': '_2FXNMst_ak'})[0].find('dl', {'class': 'XbGQRlzveO'}).get_text()
        item_nm_info = re.sub(item_nm_info_for_del, '', item_nm_info_raw)

        print('try')
    except AttributeError:
        # 리뷰에 상품 정보가 없는 경우 처리할 작업을 여기에 추가
        item_nm_info = item_nm_info_raw
        print('err')
    # 4-2-(2) re.sub() 를 활용해 dl class="XbGQRlzveO"부분부터 추출한 문장을 공백으로 대체
    #item_nm_info_for_del = reviews[review].findAll('div', {'class' : '_2FXNMst_ak'})[0].find('dl', {'class' : 'XbGQRlzveO'}).get_text()

    # 4-2-(3) re.sub(pattern, replacement, string) : string에서 pattern에 해당하는 부분을 replacement로 모두 대체
    #item_nm_info= re.sub(item_nm_info_for_del, '', item_nm_info_raw)

    # 4-2-(4) find() : 문자열 순서 (인덱스) 반환 : find()를 활용해 '제품 선택 : '이 나오는 인덱스 반환
    str_start_idx = re.sub(item_nm_info_for_del, '', item_nm_info_raw).find('제품 선택: ')

    # 4-2-(5) 제품명만 추출. strip(): 공백 제거 
    item_nm = item_nm_info[str_start_idx + 6:].strip()
    

    # 4-3. 리뷰내용 수집
    review_content_raw = reviews[review].findAll('div', {'class' : '_1kMfD5ErZ6'})[0].find('span', {'class' : '_2L3vDiadT9'}).get_text()
    review_content = re.sub(' +', ' ',re.sub('\n',' ',review_content_raw ))
    
    # 4-4. 수집데이터 저장
    write_dt_lst.append(write_dt)
    item_nm_lst.append(item_nm)
    content_lst.append(review_content)


# 현재 페이지
page_num = 1
page_ctl = 3
# 날짜 
date_cut = (datetime.now() - timedelta(days = 365)).strftime('%Y%m%d')
while True :
    print(f'start : {page_num} page 수집 중, page_ctl:{page_ctl}')
    # 1. 셀레니움으로 html가져오기
    html_source = driver.page_source
    # 2. bs4로 html 파싱
    soup = BeautifulSoup(html_source, 'html.parser')
    time.sleep(0.5)

    # 3. 리뷰 정보 가져오기
    reviews = soup.findAll('li', {'class': 'BnwL_cs1av'})


    # 4. 한페이지 내에서 수집 가능한 리뷰 리스트에 저장
    for review in range(len(reviews)):

        # 4-1.리뷰작성일자 수집
        write_dt_raw = reviews[review].findAll('span' ,{'class' : '_2L3vDiadT9'})[0].get_text()
        write_dt = datetime.strptime(write_dt_raw, '%y.%m.%d.').strftime('%Y%m%d')

        # 4-2.상품명 수집
        # 4-2-(1) 상품명이 포함된 css 선택자 입력 
        item_nm_info_raw = reviews[review].findAll('div', {'class' : '_2FXNMst_ak'})[0].get_text()

        # 4-2-(2) re.sub() 를 활용해 dl class="XbGQRlzveO"부분부터 추출한 문장을 공백으로 대체
        #item_nm_info_for_del = reviews[review].findAll('div', {'class' : '_2FXNMst_ak'})[0].find('dl', {'class' : 'XbGQRlzveO'}).get_text()
        item_nm_info_for_del = ''

        # 4-2-(3) re.sub(pattern, replacement, string) : string에서 pattern에 해당하는 부분을 replacement로 모두 대체
        item_nm_info= re.sub(item_nm_info_for_del, '', item_nm_info_raw)

        # 4-2-(4) find() : 문자열 순서 (인덱스) 반환 : find()를 활용해 '제품 선택 : '이 나오는 인덱스 반환
        str_start_idx = re.sub(item_nm_info_for_del, '', item_nm_info_raw).find('제품 선택: ')

        # 4-2-(5) 제품명만 추출. strip(): 공백 제거 
        item_nm = item_nm_info[str_start_idx + 6:].strip()


        # 4-3. 리뷰내용 수집
        review_content_raw = reviews[review].findAll('div', {'class' : '_1kMfD5ErZ6'})[0].find('span', {'class' : '_2L3vDiadT9'}).get_text()
        review_content = re.sub(' +', ' ',re.sub('\n',' ',review_content_raw ))

        # 4-4. 수집데이터 저장
        write_dt_lst.append(write_dt)
        item_nm_lst.append(item_nm)
        content_lst.append(review_content)
 
    # 리뷰 수집일자 기준 데이터 확인(최근 1년치만 수집)
    if write_dt_lst[-1] < date_cut :
        break
        
    # page 이동
    #driver.find_element(By.CSS_SELECTOR, f'#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a:nth-child({str(page_ctl)})').click()
    # driver.find_element(By.CSS_SELECTOR,f'#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a:nth-child({page_ctl})').click()
    #driver.find_element(By.XPATH, f'//*[@id="REVIEW"]/div/div[3]/div[2]/div/div/a[{page_ctl}]').click()

    #driver.find_element(By.CSS_SELECTOR,f'#REVIEW > div > div._2LvIMaBiIO > div._2g7PKvqCKe > div > div > a:nth-child({page_ctl})').click()    
    time.sleep(3)
    
    # 셀레니움으로 html가져오기
    html_source = driver.page_source
    # bs4로 html 파싱
    soup = BeautifulSoup(html_source, 'html.parser')
    time.sleep(0.5)
 
    page_num += 1
    page_ctl += 1

    # 멈춤 구문
    if page_ctl == 4:
        break


    if page_num % 10 == 1 :
        page_ctl = 3
print('done')    



result_df = pd.DataFrame({
              'RD_ITEM_NM' : item_nm_lst,
              'RD_CONTENT' : content_lst,
              'RD_WRITE_DT' : write_dt_lst })

item_name = soup.select_one('#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div._1eddO7u4UC > h3').string
result_df.to_csv(f'./result/{item_name}_review_data2.csv', index = None, encoding = 'utf-8-sig')