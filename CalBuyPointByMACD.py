# !/usr/bin/env python
# coding=utf-8
import pandas as pd
import sqlite3
import sys
from datetime import datetime
from tslib import *
# 第一个参数是数据，第二个参数是周期

workFolder = "c:\\stock\export\\stock\\"
dataBaseFolder = 'c:\\stock\\'
dataBaseName = 'stock.db'

start = datetime.now()
print(start)


def getAllStockList(dataBaseName):
    conn = sqlite3.connect(dataBaseFolder+dataBaseName)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    stockList = list(cursor.fetchall())
    #print (stockList)
    conn.close()
    return stockList


def getStockData(code, dataBaseName):
    try:
        # 打开数据库连接
        db = sqlite3.connect(dataBaseFolder+dataBaseName)
    except:
        print('Error when Connecting to DB.')
        sys.exit()
    cursor = db.cursor()
    cursor.execute('select * from stock_'+code)
    cols = cursor.description   # 返回列名
    #print (cols)
    heads = []
    # 依次把每个cols元素中的第一个值放入col数组
    for index in cols:
        heads.append(index[0])
    result = cursor.fetchall()
    df = pd.DataFrame(list(result))
    # df.drop([1,4],inplace=True)
    #print (df.tail(5))
    df.columns = heads
    db.close()
    return df


def getMACDByCode(code):
    df = getStockData(code, dataBaseName)
    stockDataFrame = calMACD(df, 12, 26, 9)
    return stockDataFrame


stockList = getAllStockList(dataBaseName)
#print (stockList)
# print(getStockData('SZ184801'))
# print(getMACDByCode('603505'))     # 去除注解以确认数据
# stockDf.drop([0,4],inplace=True)
#print (stockDf.head(5))


def BuyStockFromMACD(stockDf):
    try:
        # 规则1：这天DIF值上穿DEA
        if stockDf.iloc[-1]['DIF'] > stockDf.iloc[-1]['DEA'] and stockDf.iloc[-2]['DIF'] < stockDf.iloc[-2]['DEA']:
            # 规则2：出现红柱，即MACD值大于0
            if stockDf.iloc[-2]['MACD'] > 0:
                print(stockname)
                print("Buy Point by MACD on:" +
                      stockDf.iloc[-1]['date'] + '\t'+str(stockDf.iloc[-1]['close']))
             # 规则1：这天DIF值下穿DEA
    except:
        pass


def SellStockFromMACD(stockDf):
    try:
        # 规则1：这天DIF值上穿DEA
        if stockDf.iloc[-1]['DIF'] < stockDf.iloc[-1]['DEA'] and stockDf.iloc[-2]['DIF'] > stockDf.iloc[-2]['DEA']:
            # 规则2：Bar柱是否向下运动
            if stockDf.iloc[-1]['MACD'] < stockDf.iloc[-2]['MACD']:
                print(stockname)
                print("Sell Point by MACD on:" +
                      stockDf.iloc[-1]['date'] + '\t'+str(stockDf.iloc[-1]['close']))
    except:
        pass


for stockname in stockList:
    codename = str(stockname)
    #print (codename)
    stockcode = codename[8:16]
    #print (stockcode)
    df = getStockData(stockcode, dataBaseName)
    #df = getStockData(stockname)
    stockDf = getMACDByCode(stockcode)
    print(stockname)
    print(stockDf.tail(5))
    BuyStockFromMACD(stockDf)
