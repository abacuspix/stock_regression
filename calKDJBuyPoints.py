# !/usr/bin/env python
# coding=utf-8
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import sys
# 计算KDJ


def calKDJ(df):
    df['MinLow'] = df['low'].rolling(9, min_periods=9).min()
    # 填充NaN数据
    df['MinLow'].fillna(value=df['low'].expanding().min(), inplace=True)
    df['MaxHigh'] = df['high'].rolling(9, min_periods=9).max()
    df['MaxHigh'].fillna(value=df['high'].expanding().max(), inplace=True)
    df['RSV'] = (df['close'] - df['MinLow']) / \
        (df['MaxHigh'] - df['MinLow']) * 100
    for i in range(len(df)):
        if i == 0:    # 第一天
            df.loc[i, 'K'] = 50
            df.loc[i, 'D'] = 50
        if i > 0:
            df.loc[i, 'K'] = df.loc[i-1, 'K']*2/3 + 1/3*df.loc[i, 'RSV']
            df.loc[i, 'D'] = df.loc[i-1, 'D']*2/3 + 1/3*df.loc[i, 'K']
        df.loc[i, 'J'] = 3*df.loc[i, 'K']-2*df.loc[i, 'D']
    return df


def calRSI(df, periodList):
    # 计算和上一个交易日收盘价的差值
    df['diff'] = df["close"]-df["close"].shift(1)
    df['diff'].fillna(0, inplace=True)
    df['up'] = df['diff']
    # 过滤掉小于0的值
    df['up'][df['up'] < 0] = 0
    df['down'] = df['diff']
    # 过滤掉大于0的值
    df['down'][df['down'] > 0] = 0
    # 通过for循环，依次计算periodList中不同周期的RSI等值
    for period in periodList:
        df['upAvg'+str(period)] = df['up'].rolling(period).sum()/period
        df['upAvg'+str(period)].fillna(0, inplace=True)
        df['downAvg'+str(period)
           ] = abs(df['down'].rolling(period).sum()/period)
        df['downAvg'+str(period)].fillna(0, inplace=True)
        df['RSI'+str(period)] = 100 - 100 / \
            ((df['upAvg'+str(period)]/df['downAvg'+str(period)]+1))
    return df


def getSockDataFromDB(code):
    try:
        # 打开数据库连接
        db = sqlite3.connect('etf.db')
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


def printKDJBuyPoints(code):
    df = getSockDataFromDB(code)
    stockDf = calKDJ(df)
    cnt = 0
    buyDate = ''
    while cnt <= len(stockDf)-1:
        if (cnt >= 5):     # 略过前几天的误差
            # 规则1：前一天J值大于10，当天J值小于10，是买点、
            if stockDf.iloc[cnt]['J'] < 10 and stockDf.iloc[cnt-1]['J'] > 10:
                buyDate = buyDate+stockDf.iloc[cnt]['date'] + ','
                cnt = cnt+1
                continue
            # 规则2：K,D均在20之下，出现K线上穿D线的金叉现象
            # 规则1和规则2是“或”的关系，所以当满足规则1时直接continue
            if stockDf.iloc[cnt]['K'] > stockDf.iloc[cnt]['D'] and stockDf.iloc[cnt-1]['D'] > stockDf.iloc[cnt-1]['K']:
                # 满足上穿条件后再判断K和D均小于20
                if stockDf.iloc[cnt]['K'] < 20 and stockDf.iloc[cnt]['D'] < 20:
                    print("Buy Point on:" + df.iloc[cnt]['date'])
        cnt = cnt+1


def printRSIBuyPoints(code):
    LIST = [6, 12, 24]    # 周期列表
# 调用方法计算RSI
    stockDataFrame = calRSI(getSockDataFromDB(code), LIST)
    cnt = 0
    buyDate = ''
    while cnt <= len(stockDataFrame)-1:
        if (cnt >= 30):    # 前几天有误差，从第30天算起
            try:
                # 规则1：这天RSI6低于20
                if stockDataFrame.iloc[cnt]['RSI6'] < 50:
                    # 规则2.1：当天RSI6上穿RSI12
                    if stockDataFrame.iloc[cnt]['RSI6'] > stockDataFrame.iloc[cnt]['RSI12'] and stockDataFrame.iloc[cnt-1]['RSI6'] < stockDataFrame.iloc[cnt-1]['RSI12']:
                        #buyDate = buyDate+stockDataFrame.iloc[cnt]['date'] + ','
                        print("Buy Point by RSI on:" +
                              stockDataFrame.iloc[cnt]['Date'])
                    # 规则2.2：当天RSI6上穿RSI24
                    if stockDataFrame.iloc[cnt]['RSI6'] > stockDataFrame.iloc[cnt]['RSI24'] and stockDataFrame.iloc[cnt-1]['RSI6'] < stockDataFrame.iloc[cnt-1]['RSI24']:
                        #buyDate = buyDate+stockDataFrame.iloc[cnt]['date'] + ','
                        print("Buy Point by RSI on:" +
                              stockDataFrame.iloc[cnt]['date'])
            except:
                pass
        cnt = cnt+1


def printRSISellPoints(code):
    LIST = [6, 12, 24]    # 周期列表
    # 调用方法计算RSI
    stockDataFrame = calRSI(getSockDataFromDB(code), LIST)
    cnt = 0
    sellDate = ''
    while cnt <= len(stockDataFrame)-1:
        if (cnt >= 30):    # 前几天有误差，从第30天算起
            try:
                # 规则1：这天RSI6高于80
                if stockDataFrame.iloc[cnt]['RSI6'] < 80:
                    # 规则2.1：当天RSI6下穿RSI12
                    if stockDataFrame.iloc[cnt]['RSI6'] < stockDataFrame.iloc[cnt]['RSI12'] and stockDataFrame.iloc[cnt-1]['RSI6'] > stockDataFrame.iloc[cnt-1]['RSI12']:
                        print("Sell Point by RSI on:" +
                              stockDataFrame.iloc[cnt]['date'])
                    # 规则2.2：当天RSI6下穿RSI24
                    if stockDataFrame.iloc[cnt]['RSI6'] < stockDataFrame.iloc[cnt]['RSI24'] and stockDataFrame.iloc[cnt-1]['RSI6'] > stockDataFrame.iloc[cnt-1]['RSI24']:
                        if sellDate.index(stockDataFrame.iloc[cnt]['date']) == -1:
                            print("Sell Point by RSI on:" +
                                  stockDataFrame.iloc[cnt]['date'])
            except:
                pass
        cnt = cnt+1


# printRSISellPoints('SH510050')
printKDJBuyPoints('SH510050')
