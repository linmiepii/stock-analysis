#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 19:40:17 2020

@author: linmiepii
"""

# step1. import package 
import requests
import pandas as pd
import numpy as np
from io import StringIO
import sqlite3                                      #先抓入這個套件
from datetime import datetime
from datetime import date
from datetime import time
import time as t




conn = sqlite3.connect('../data/stock.sqlite3')  #用connect 跟資料庫做連結 資料庫名稱為



# step2. 進入目標網站,爬取盤後資訊
startDay = '20181030'
datelist = pd.date_range(datetime.strptime(startDay,'%Y%m%d'),date.today()).strftime('%Y%m%d').tolist()

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

for dateStr in datelist:
    try:
        r = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + dateStr + '&type=ALL', headers = headers)
    except Exception as e:
        print('*** Warning: can not get price at' + dateStr)
        print(e)

    
    # step3. 篩選出個股盤後資訊
    str_list = []
    for i in r.text.split('\n'):
        if len(i.split('",')) == 17 and i[0] != '=':       
            i = i.strip(",\r\n")
            str_list.append(i) 

    
    if str_list:
    # step4. 印出選股資訊
        df = pd.read_csv(StringIO("\n".join(str_list)))  
        df['date'] = dateStr
        # pd.set_option('display.max_rows', None)
        
        
        df.to_sql('daily_price', conn,   if_exists='append') 
        print(dateStr + " data is sent in sql")
        ### 將資料存為 daily_price  ##然後連到上一行 所說的conn 
        ### if_exists='replace' 是說如果 資料本來就存在的話就取代掉
        ### to_sql 當然就是說把csv 轉成sql囉
    else:
        print(dateStr + " no data today")
    
    t.sleep(3)
