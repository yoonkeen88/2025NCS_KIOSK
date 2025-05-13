import urllib.request
import urllib.parse
import json
import requests
import os
import pandas as pd

from bs4 import BeautifulSoup
# 1. urllib

for i in range(1,49):
    url = f'https://www.hollys.co.kr/store/korea/korStore2.do?pageNo={i}&sido=&gugun=&store='

    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    tbody = soup.find('tbody')
    rows = tbody.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])  # Get rid of empty values
    df = pd.DataFrame(data, columns=['번호', '지점명', '주소', '전화번호', '상세보기'])
    df.to_csv(f'hollys_{i}.csv', index=False, encoding='utf-8-sig') 
    print(f"save complete {i}")