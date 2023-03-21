# !/usr/bin/env python
# coding=utf-8
import sqlite3
import sys,os
import tushare as ts
import pandas as pd
import pandas_datareader
try:
    # 打开数据库连接
    connection = sqlite3.connect('stock.db')
except:
    print('Error when Connecting to DB.')
    sys.exit()
cursor = connection.cursor()
# 从网站爬取数据，并插入到对应的数据表中


def insertStockData(code, startDate, endDate):
    try:
        #filename = 'c:\\stock\\'+code+'.csv'
        stock = pandas_datareader.get_data_yahoo(code+'.ss', startDate, endDate)
        stock.to_csv('c:\\stock\\temp\\'+code+'.csv')
        filename = 'c:\\stock\\temp\\'+code+'.csv'
        if(len(stock) < 1):
            stock = pandas_datareader.get_data_yahoo(code+'.ss', startDate, endDate)
        # 删除最后一行，因为get_data_yahoo会多取一天的股票交易数据
        #stock.drop(stock.index[len(stock)-1], inplace=True)        # 在本地留份csv
        
        print('Current handle:' + code)
        #stock.to_csv(filename)
        db = pd.read_csv(filename, encoding='gbk')
        #print (db.head(5))
        db.to_sql("stock_"+code, connection, if_exists="append",index=False)
        connection.commit()
    except Exception as e:
        print('Error when inserting the data of:' + code)
        print(repr(e))
        connection.rollback()


startDate = '2010-01-01'
endDate = '2022-8-19'
#stockList = ['601318']
stockList = os.listdir("c:\\stock\\stock\\")

for code in stockList:
    stock_code=code[2:8]
    print (stock_code)
    #stock_code=int(stock_code)
    insertStockData(code, startDate, endDate)
'''            
stockList=ts.get_stock_basics()  # 通过tushare接口获取股票代码
for code in stockList.index:
    insertStockData(code,startDate,endDate)            
'''
cursor.close()
connection.close()
