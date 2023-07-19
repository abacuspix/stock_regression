# !/usr/bin/env python
# coding=utf-8
import pandas as pd
import sqlite3
import sys

# 计算RSI的方法，输入参数periodList传入周期列表 
def calRSI(df,periodList):
    # 计算和上一个交易日收盘价的差值
    df['diff'] = df["close"]-df["close"].shift(1) 
    df['diff'].fillna(0, inplace = True)    
    df['up'] = df['diff']
    # 过滤掉小于0的值
    df['up'][df['up']<0] = 0
    df['down'] = df['diff']
    # 过滤掉大于0的值
    df['down'][df['down']>0] = 0
    # 通过for循环，依次计算periodList中不同周期的RSI等值
    for period in periodList:
        df['upAvg'+str(period)] = df['up'].rolling(period).sum()/period
        df['upAvg'+str(period)].fillna(0, inplace = True)
        df['downAvg'+str(period)] = abs(df['down'].rolling(period).sum()/period)
        df['downAvg'+str(period)].fillna(0, inplace = True)
        df['RSI'+str(period)] = 100 - 100/((df['upAvg'+str(period)]/df['downAvg'+str(period)]+1))
    return df

def getSockDataFromDB(code):
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
    #print (df.head(5))
    df.columns = heads
    # delete the last colume
    df.drop([len(df)-1], inplace=True)
    #print (df.tail(5))
    return df

LIST = [6,12,24]    # 周期列表

# 调用方法计算RSI
stockDataFrame = calRSI(getSockDataFromDB('NVDA'),LIST) 
cnt=0    
sellDate=''
while cnt<=len(stockDataFrame)-1:
    if(cnt>=30):    # 前几天有误差，从第30天算起
        try:        
            # 规则1：这天RSI6高于80
            if stockDataFrame.iloc[cnt]['RSI6']<80:
                # 规则2.1：当天RSI6下穿RSI12
                if  stockDataFrame.iloc[cnt]['RSI6']<stockDataFrame.iloc[cnt]['RSI12'] and stockDataFrame.iloc[cnt-1]['RSI6']>stockDataFrame.iloc[cnt-1]['RSI12']:
                    print("Sell Point by RSI on:" + stockDataFrame.iloc[cnt]['date'])
                    # 规则2.2：当天RSI6下穿RSI24
                if  stockDataFrame.iloc[cnt]['RSI6']<stockDataFrame.iloc[cnt]['RSI24'] and stockDataFrame.iloc[cnt-1]['RSI6']>stockDataFrame.iloc[cnt-1]['RSI24']:
                    if sellDate.index(stockDataFrame.iloc[cnt]['date']) == -1:
                        print("Sell Point by RSI on:" + stockDataFrame.iloc[cnt]['date'])
        except:
            pass                
    cnt=cnt+1

