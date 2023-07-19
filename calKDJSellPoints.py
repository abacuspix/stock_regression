# !/usr/bin/env python
# coding=utf-8
import pandas as pd
import pandas_datareader
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
        #print(df.tail(5))
    return df
# 绘制KDJ线
# 从API中获取股票数据


def getStockDataFromAPI(stockCode, startDate, endDate):
    try:
        # 给股票代码加ss前缀来获取上证股票的数据
        stock = pandas_datareader.get_data_yahoo(
            stockCode+'.ss', startDate, endDate)
        if (len(stock) < 1):
            # 如果没取到数据，则抛出异常
            raise Exception()
        # 删除最后一行，因为get_data_yahoo会多取一天的股票交易数据
        stock.drop(stock.index[len(stock)-1], inplace=True)  # 在本地留份csv
        filename = 'D:\\stockData\ch9\\'+stockCode+startDate+endDate+'.csv'
        stock.to_csv(filename)
    except Exception as e:
        print('Error when getting the data of:' + stockCode)
        print(repr(e))
# 设置tkinter窗口


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


def printSellPoints(code):
    df = getSockDataFromDB(code)
    stockDf = calKDJ(df)
    cnt = 0
    buyDate = ''
    while cnt <= len(stockDf)-1:
        if (cnt >= 5):  # 略过前几天的误差
            # 规则1：前一天J值大于90，当天J值小于90，是Mai点、
            if stockDf.iloc[cnt]['J'] > 90 and stockDf.iloc[cnt-1]['J'] < 90:
                buyDate = buyDate+stockDf.iloc[cnt]['date'] + ','
                cnt = cnt+1
                continue
            # 规则2：K,D均在20之下，出现K线上穿D线的金叉现象
            # 规则1和规则2是“或”的关系，所以当满足规则1时直接continue
            if stockDf.iloc[cnt]['K'] < stockDf.iloc[cnt]['D'] and stockDf.iloc[cnt-1]['D'] < stockDf.iloc[cnt-1]['K']:
                # 满足上穿条件后再判断K和D均小于20
                if stockDf.iloc[cnt]['K'] > 90 and stockDf.iloc[cnt]['D'] < 90:
                    print("Sell Point on:" + df.iloc[cnt]['date'])
        cnt = cnt+1


printSellPoints('NVDA')
