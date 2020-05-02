#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  1 10:12:12 2020

@author: linmiepii
"""

#!/usr/bin/python
import sqlite3 
import pandas as pd
import sys
from colorama import Fore
from colorama import Style

conn = sqlite3.connect('../data/stock.sqlite3')
deal_info = sys.argv[1:6]
df = pd.DataFrame(deal_info)
df = df.transpose()
df.columns = ['date','deal_type', '證券代號', 'qty','price']


#%Y%m%d
date = deal_info[0]        

#buy or sell
deal_type = deal_info[1]   
stock_no = deal_info[2]
qty = deal_info[3]
price = deal_info[4]

df.to_sql('deal', conn, if_exists='append') 
print(df)
print (f'*** dela information *** {Fore.GREEN}{date}{Style.RESET_ALL}, you {deal_type} #{stock_no} qty:{qty} at ${price}')  



