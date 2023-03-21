# !/usr/bin/env python
# coding=utf-8
import sqlite3
import sys
import os
import tushare as ts
try:
    # 打开数据库连接
    db = sqlite3.connect('stock.db')
except:
    print('Error when Connecting to DB.')
    sys.exit()
cursor = db.cursor()
'''
stockList=['600895','603982','300097','603505','600759']
for code in stockList:
    try:
        createSql= 'CREATE TABLE stock_' +code+' (  date varchar(255) ,Open float,Close float ,High float , low float,vol int(11))'        
        cursor.execute(createSql)
    except:
        print('Error when Creating table for:' + code)
'''

'''for x in os.listdir("c:\\stock\\export\\stock\\"):
    if x.endswith(".csv"):
        # Prints only text file present in My Folder
        t=(x[0:8])
        print (t)'''
stockList = os.listdir("c:\\stock\\export\\stock\\")
for code in stockList:
    print(code)
    try:
        createSql = 'CREATE TABLE stock_' + code[2:8] + \
            ' (Date varchar(255) , High float, Low float, Open float, Close float, Volume int(11), "Adj Close" float)'
        print(createSql)
        cursor.execute(createSql)
    except:
        print('Error when Creating table for:' + code)
db.commit()
cursor.close()
db.close()
