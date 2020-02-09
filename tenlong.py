def showpage(url, kind):
    html = requests.get(url,headers = headers).text
    soup = BeautifulSoup(html, 'html.parser')
    res = soup.find_all("div",{"class":"list-wrapper"})[0]
    items = res.select('.single-book')                                         # 所有item                                                                      # 計算該分頁有幾本書                        
    for item in items:
        src = item.select('a img')[0]["src"]
        title = item.select('.title a')[0].text                                # 書名
        imgurl = src.split(".?")[-1]                                           # 圖片網址
        pricing = item.select('.pricing')[0].text                              # 價格
         # 將資料加入list1串列中
        listdata = [title, imgurl, pricing]
        list1.append(listdata)
        print("\n書名:"+ title)
        print("圖片網址:"+ imgurl)
        print(pricing)



import requests
from bs4 import BeautifulSoup
import openpyxl

homeurl = 'https://www.tenlong.com.tw/categories/web-crawler'               
headers ={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chorme/64.0.3282.186 Safari/537.36'
        }                         
html = requests.get(homeurl, headers = headers).text                           # 傳回去除所有HTML標籤後的網頁文字內容
soup = BeautifulSoup(html, 'html.parser')
pages = int(soup.select(".pagination.pagination-footer a")[-2].text)           # 爬蟲分類有多少頁（id不可有空格！！！！）
print("共有",pages,"頁")

workbook = openpyxl.Workbook()                                                 # 建立一個工作簿
sheet = workbook.worksheets[0]                                                 # 獲取工作表
list1 = []

for page in range(1,pages+1):
    pageurl = homeurl + '?page=' + str(page).strip()                           # 刪除字串頭尾的指定符號並產生新字串
    print("第",page,"頁",pageurl)
    showpage(pageurl,kind)

# excel資料
listtitle = ["書名","圖片網址","價格"]
sheet.append(listtitle)                                                        # 加入標題
for item1 in list1:
    sheet.append(item1)
    
workbook.save('tenlong.xlsx')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 13:47:20 2020

@author: cosmo
"""

