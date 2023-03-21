# !/usr/bin/env python
# coding=utf-8
import pandas as pd
import sqlite3
import sys
# 第一个参数是数据，第二个参数是周期


def calEMA(df, term):
    for i in range(len(df)):
        if i == 0:    # 第一天
            df.loc[i, 'EMA'] = df.loc[i, 'close']
        if i > 0:
            df.loc[i, 'EMA'] = (term-1)/(term+1) * \
                df.loc[i-1, 'EMA']+2/(term+1)*df.loc[i, 'close']
    EMAList = list(df['EMA'])
    return EMAList
# 定义计算MACD的方法


def calMACD(df, shortTerm=12, longTerm=26, DIFTerm=9):
    shortEMA = calEMA(df, shortTerm)
    longEMA = calEMA(df, longTerm)
    df['DIF'] = pd.Series(shortEMA) - pd.Series(longEMA)
    for i in range(len(df)):
        if i == 0:    # 第一天
            df.loc[i, 'DEA'] = df.loc[i, 'DIF']     # LOC可以通过标签名和索引来获取数据
        if i > 0:
            df.loc[i, 'DEA'] = (DIFTerm-1)/(DIFTerm+1) * \
                df.loc[i-1, 'DEA'] + 2/(DIFTerm+1)*df.loc[i, 'DIF']
    df['MACD'] = 2*(df['DIF'] - df['DEA'])
    #print (df.tail(5))
    return df


def getMACDByCode(code):
    try:
        # 打开数据库连接
        db = sqlite3.connect('stock.db')
    except:
        print('Error when Connecting to DB.')
        sys.exit()
    cursor = db.cursor()
    cursor.execute('select * from stock_'+code)
    cols = cursor.description   # 返回列名
    heads = []
    # 依次把每个cols元素中的第一个值放入col数组
    for index in cols:
        heads.append(index[0])
    result = cursor.fetchall()
    df = pd.DataFrame(list(result))
    df.columns = heads
    stockDataFrame = calMACD(df, 12, 26, 9)
    return stockDataFrame


stockDf = getMACDByCode('SH601318')
#print (stockDf.tail(5))
cnt = 0
while cnt <= len(stockDf)-1:
    if (cnt >= 30):    # 前几天有误差，从第30天算起
        try:
            # 规则1：这天DIF值下穿DEA
            #print (stockDf.iloc[cnt]['DIF'], stockDf.iloc[cnt]['MACD'])
            if stockDf.iloc[cnt]['DIF'] < stockDf.iloc[cnt]['DEA'] and stockDf.iloc[cnt-1]['DIF'] > stockDf.iloc[cnt-1]['DEA']:
                # 规则2：Bar柱是否向下运动
                if stockDf.iloc[cnt]['MACD'] < stockDf.iloc[cnt-1]['MACD']:
                    print("Sell Point by MACD on:" +
                          stockDf.iloc[cnt]['date'] + '\t'+str(stockDf.iloc[cnt]['close']))
        # 规则1：这天DIF值上穿DEA
            if stockDf.iloc[cnt]['DIF'] > stockDf.iloc[cnt]['DEA'] and stockDf.iloc[cnt-1]['DIF'] < stockDf.iloc[cnt-1]['DEA']:
                # 规则2：出现红柱，即MACD值大于0
                if stockDf.iloc[cnt]['MACD'] > 0:
                    print("Buy Point by MACD on:" +
                          stockDf.iloc[cnt]['date'] + '\t'+str(stockDf.iloc[cnt]['close']))
             # 规则1：这天DIF值下穿DEA
        except:
            pass
    cnt = cnt+1
