import requests
from bs4 import BeautifulSoup
import openpyxl

# 判斷頁數
def showbook(kindurl,kind):
    html = requests.get(kindurl,headers = headers).text
    soup = BeautifulSoup(html, 'html.parser')
    res = soup.select((".pagination.pagination-footer a"))                     # 屬性內容不要有空格
    check_final_page = soup.find('a', {'rel':'next'})
    if res != []:                                                              # 表示有分頁
        page = int(soup.select(".pagination.pagination-footer a")[-2].text)
        while check_final_page != None:                                        # 檢查是否仍有下一頁
            final_page = str(page).strip()                                     # 刪除字串頭尾的指定符號
            newurl = kindurl + '?page=' + final_page                    
            new_html = requests.get(newurl,headers = headers).text
            new_soup = BeautifulSoup(new_html, 'html.parser')
            check_final_page = new_soup.find('a', {'rel':'next'})
            # 處理兩個分頁時page[-2]為文字之狀況
            if len(new_soup.select(".pagination.pagination-footer a")) > 2: 
                page = int(new_soup.select(".pagination.pagination-footer a")\
                           [-2].text)                               
        
        print("%s"%kind,"分類共有",final_page,"頁")
        for page in range(1,page+1):
            pageurl = kindurl + '?page=' + str(page)                           
            print("第",page,"頁",pageurl)
            showpage(pageurl,kind)
    else:                                                                      # 沒有分頁的處理
        print("%s無分頁"%kind)
        showpage(kindurl, kind)         

# 存取各頁書籍資料
def showpage(url, kind):
    html = requests.get(url,headers = headers).text
    soup = BeautifulSoup(html, 'html.parser')
    res = soup.find("div",{"class":"list-wrapper"})
    items = res.select('.single-book')                                         # 所有書                                                                      # 計算該分頁有幾本書                        
    for item in items:
        src = item.select('a img')[0]["src"]                                   # 圖片網址
        title = item.select('.title')[0].text                                  # 書名
        pricing = item.select('.pricing')[0].text                              # 價格
        # 將資料加入list1串列中
        listdata = [title, src, pricing]
        list1.append(listdata)
        print("\n書名:", title)
        print("圖片網址:", src)
        print("價格", pricing)

# main code
mainurl = 'https://www.tenlong.com.tw/categories/data-science'               
headers ={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko)Chorme/64.0.3282.186\
        Safari/537.36'
        }
url = "https://www.tenlong.com.tw/"                         
html = requests.get(mainurl, headers = headers).text                           # 傳回去除所有HTML標籤後的網頁文字內容
soup = BeautifulSoup(html, 'html.parser')
res = soup.find('ul', {'class':'link-list'})                                   # 回傳<ul class:link-list>內容（字串）
kinds = res.select("a")                                                        # 回傳res內標籤a的內容(串列)

#取得分類數
kindsurl = []
for i in range(len(kinds)):
    kindsurl.append(kinds[i].get("href")) 
kindno = len(kinds)-1                                                          # 取得有多少分類
print("共有",kindno,"分類")

# 建立excel檔案
workbook = openpyxl.Workbook()                                                 # 建立一個工作簿
sheet = workbook.worksheets[0]                                                 # 獲取工作表
list1 = []

# 取得分類網址
for i in range(1, len(kindsurl)):
    kindurl = "%s%s"%(url, kindsurl[i])                                        # 分類網址
    kind = kinds[i].text                                                       # 分類名稱
    print(kind)
    print(kindurl)                                                        
    showbook(kindurl, kind)                                                    

#存成excel資料
listtitle = ["書名","圖片網址","價格"]
sheet.append(listtitle)                                                        # 加入標題
for item1 in list1:
    sheet.append(item1)
    
workbook.save('tenlong_v2.xlsx')

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 13:47:20 2020

@author: cosmo
"""

