# !/usr/bin/env python
# coding=utf-8
import datetime
import time
from datetime import datetime
from tslib import *

dataBaseName = 'c:\\stock\\stock.db'
ts = time.time()
start = datetime.now()
logName = "choosed_stock_"+str(ts)+".txt"
print(start)
stockList = getAllStockList(dataBaseName)
#print (stockList)
start = datetime.now()


def chooseStockFromMA500(stockList):
    with open(logName, 'a') as f:
        f.write(str(datetime.now())+'\n')
        f.write('====================MA500===============================\n')
    for stockname in stockList:
        df = getStockData(stockname, dataBaseName)
        MA_5 = calMA(df, 5)
        MA_13 = calMA(df, 13)
        MA_55 = calMA(df, 55)
        MA_89 = calMA(df, 89)
        MA_120 = calMA(df, 120)
        MA_250 = calMA(df, 250)
        MA_500 = calMA(df, 500)
        if (df.iloc[-1]['close'] - df.iloc[-1]['MA_500'])/df.iloc[-1]['MA_500'] > 0 \
                and (df.iloc[-1]['close'] - df.iloc[-1]['MA_500'])/df.iloc[-1]['MA_500']*100 < 5\
                and (HighMax(df, 120)-df.iloc[-1]['close'])/HighMax(df, 120)*100 > 50:
            with open(logName, 'a') as f:
                f.write(''.join(stockname)+'\n')


def chooseStockFromMA250(stockList):
    with open(logName, 'a') as f:
        f.write(str(datetime.now())+'\n')
        f.write('=================MA250====================================\n')
    for stockname in stockList:
        df = getStockData(stockname, dataBaseName)
        MA_5 = calMA(df, 5)
        MA_13 = calMA(df, 13)
        MA_55 = calMA(df, 55)
        MA_89 = calMA(df, 89)
        MA_120 = calMA(df, 120)
        MA_250 = calMA(df, 250)
        MA_500 = calMA(df, 500)
        if (df.iloc[-1]['close'] - df.iloc[-1]['MA_250'])/df.iloc[-1]['MA_250'] > 0 \
                and (df.iloc[-1]['close'] - df.iloc[-1]['MA_250'])/df.iloc[-1]['MA_250']*100 < 5\
                and (HighMax(df, 120)-df.iloc[-1]['close'])/HighMax(df, 120)*100 > 50:
            with open(logName, 'a') as f:
                f.write(''.join(stockname)+'\n')

def chooseStockFromMA120(stockList):
    with open(logName, 'a') as f:
        f.write(str(datetime.now())+'\n')
        f.write('=================MA120====================================\n')
    for stockname in stockList:
        df = getStockData(stockname, dataBaseName)
        MA_5 = calMA(df, 5)
        MA_13 = calMA(df, 13)
        MA_55 = calMA(df, 55)
        MA_89 = calMA(df, 89)
        MA_120 = calMA(df, 120)
        MA_250 = calMA(df, 250)
        MA_500 = calMA(df, 500)
        if (df.iloc[-1]['close'] - df.iloc[-1]['MA_120'])/df.iloc[-1]['MA_120'] > 0 \
                and (df.iloc[-1]['close'] - df.iloc[-1]['MA_120'])/df.iloc[-1]['MA_120']*100 < 5\
                and (HighMax(df, 120)-df.iloc[-1]['close'])/HighMax(df, 120)*100 > 50:
            with open(logName, 'a') as f:
                f.write(''.join(stockname)+'\n')


def chooseStockFromMA55(stockList):
    with open(logName, 'a') as f:
        f.write(str(datetime.now())+'\n')
        f.write('=================MA55====================================\n')
    for stockname in stockList:
        df = getStockData(stockname, dataBaseName)
        MA_5 = calMA(df, 5)
        MA_13 = calMA(df, 13)
        MA_55 = calMA(df, 55)
        MA_89 = calMA(df, 89)
        MA_120 = calMA(df, 120)
        MA_250 = calMA(df, 250)
        MA_500 = calMA(df, 500)
        #print (stockname, df.iloc[-1]['close'], df.iloc[-2]['close'])
        if (df.iloc[-1]['close'] - df.iloc[-1]['MA_55']) > 0 \
                and (df.iloc[-2]['close'] - df.iloc[-2]['MA_55']) < 0\
                and (df.iloc[-1]['MA_13']-df.iloc[-1]['MA_55']) > 0\
                and (df.iloc[-2]['MA_13']-df.iloc[-2]['MA_55']) < 0:
            with open(logName, 'a') as f:
                f.write(''.join(stockname)+'\n')


stockList = getAllStockList(dataBaseName)
#print (stockList)
chooseStockFromMA55(stockList)
chooseStockFromMA120(stockList)
chooseStockFromMA250(stockList)
chooseStockFromMA500(stockList)

# finished the report
with open(logName, 'a') as f:
    f.write('==========================================================\n')
delta = datetime.now() - start
print("Program elapsed time in seconds", delta.seconds)
