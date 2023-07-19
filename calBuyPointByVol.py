# !/usr/bin/env python
# coding=utf-8
import pandas as pd
import numpy as np
import sqlite3
import sys
# 涨幅是否大于指定比率


def isMoreThanPer(lessVal, highVal, per):
    if np.abs(highVal-lessVal)/lessVal > per/100:
        return True
    else:
        return False
# 涨幅是否小于指定比率


def isLessThanPer(lessVal, highVal, per):
    if np.abs(highVal-lessVal)/lessVal < per/100:
        return True
    else:
        return False


def getStockData(code):
    try:
        # 打开数据库连接
        db = sqlite3.connect('us_stock.db')
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
    print(df.tail(5))
    df.columns = heads
    return df


# 本次直接从文件中读取数据
#df = pd.read_csv('c:/stock/export/STOCK/SH601318.csv',skiprows=[0,1],names=("Date","Open","High","Low","Close","Volume","vol2"), encoding='gbk')
# delete the last colume
df = getStockData('NVDA')
cnt = 0
while cnt <= len(df)-1:
    try:
        # 规则1：连续三天收盘价变动不超过3%
        if isLessThanPer(df.iloc[cnt]['close'], df.iloc[cnt+1]['close'], 3) and isLessThanPer(df.iloc[cnt]['close'], df.iloc[cnt+2]['close'], 3):
            # 规则2：连续三天成交量涨幅超过75%
            if isMoreThanPer(df.iloc[cnt]['volume'], df.iloc[cnt+1]['volume'], 75) and isMoreThanPer(df.iloc[cnt]['volume'], df.iloc[cnt+2]['volume'], 75):
                print("Buy Point on:" + df.iloc[cnt] + ['date'], df.iloc[cnt]['close'])
        if isLessThanPer(df.iloc[cnt]['close'], df.iloc[cnt+1]['close'], 3) and isLessThanPer(df.iloc[cnt]['close'], df.iloc[cnt+2]['close'], 3):
            # 规则2：连续三天成交量跌幅超过75%
            if isMoreThanPer(df.iloc[cnt+1]['volume'], df.iloc[cnt]['volume'], 75) and isMoreThanPer(df.iloc[cnt+2]['volume'], df.iloc[cnt]['volume'], 75):
                print("Sell Point on:" + df.iloc[cnt]['date'], df.iloc[cnt]['close'])
    except:
        pass
    cnt = cnt+1
