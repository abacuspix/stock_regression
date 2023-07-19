import pandas as pd
import sqlite3
import sys
import datetime
import sys
from datetime import datetime


def getStockData(code, dataBaseName):
    try:
        # 打开数据库连接
        db = sqlite3.connect(dataBaseName)
    except:
        print('Error when Connecting to DB.')
        sys.exit()
    cursor = db.cursor()
    cursor.execute('select * from '+code)
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


def getAllStockList(dataBaseName):
    codeList = []
    conn = sqlite3.connect(dataBaseName)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    stockList = list(cursor.fetchall())
    conn.close()
    for stockname in stockList:
        #print (type(filename))
        codename = str(stockname)
        #print (codename)
        #stockcode = str(filename[0:8])
        codename = codename[2:-3]
        #print (codename)
        codeList.append(codename)
    return codeList


def calMA(df, maInterval):
    df['MA_' + str(maInterval)] = df['close'].rolling(window=maInterval).mean()
    return df


def HighMax(df, days):
    return (max(df.iloc[-days:]['high']))


def LowMin(df, days):
    return (min(df.iloc[-days:]['low']))


def calEMA(df, term):
    #print (df.head(5))
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
            df.loc[i, 'DEA'] = df.loc[i, 'DIF']     # ix可以通过标签名和索引来获取数据
        if i > 0:
            df.loc[i, 'DEA'] = (DIFTerm-1)/(DIFTerm+1) * \
                df.loc[i-1, 'DEA'] + 2/(DIFTerm+1)*df.loc[i, 'DIF']
    df['MACD'] = 2*(df['DIF'] - df['DEA'])
    return df


def printMAbuyPoint(df):
    maIntervalList = [3, 5, 10]
    # 虽然在后文中只用到了5日均线，但这里演示设置3种均线
    for maInterval in maIntervalList:
        df['MA_' + str(maInterval)
           ] = df['close'].rolling(window=maInterval).mean()
    cnt = 0
    while cnt <= len(df)-1:
        #print("cnt check:" + df.iloc[cnt]['date']+ '--->'+ str(df.iloc[cnt]['close']))
        try:
            # BUY 规则1：收盘价连续三天上扬
            if df.iloc[cnt]['close'] < df.iloc[cnt+1]['close'] and df.iloc[cnt+1]['close'] < df.iloc[cnt+2]['close']:
                # 规则2：5日均线连续三天上扬
                if df.iloc[cnt]['MA_5'] < df.iloc[cnt+1]['MA_5'] and df.iloc[cnt+1]['MA_5'] < df.iloc[cnt+2]['MA_5']:
                    # 规则3：第3天收盘价上穿5日均线
                    if df.iloc[cnt+1]['MA_5'] > df.iloc[cnt]['close'] and df.iloc[cnt+2]['MA_5'] < df.iloc[cnt+1]['close']:
                        print(
                            "Buy Point on:" + df.iloc[cnt]['date'] + '--->' + str(df.iloc[cnt]['close']))
         # SALE 规则1，收盘价连续三天下跌
            if df.iloc[cnt]['close'] > df.iloc[cnt+1]['close'] and df.iloc[cnt+1]['close'] > df.iloc[cnt+2]['close']:
                # 规则2，5日均线连续三天下跌
                if df.iloc[cnt]['MA_5'] > df.iloc[cnt+1]['MA_5'] and df.iloc[cnt+1]['MA_5'] > df.iloc[cnt+2]['MA_5']:
                    # 规则3，第3天收盘价下穿5日均线
                    if df.iloc[cnt+1]['MA_5'] < df.iloc[cnt]['close'] and df.iloc[cnt+2]['MA_5'] > df.iloc[cnt+1]['close']:
                        print(
                            "Sell Point on:" + df.iloc[cnt]['date'] + '--->' + str(df.iloc[cnt]['close']))
        except:  # 有几天是没有5日均线的，所以用except处理异常
            pass
        cnt = cnt+1
