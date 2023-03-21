# coding=utf-8
import tushare as ts
from tslib import *
import time

dataBaseName = 'c:\\stock\\etf.db'
t = time.time()
start = datetime.now()
logName="choosed_stock_"+str(ts)+".txt"
print (start)
stockList = getAllStockList(dataBaseName)
#print (stockList)
for codename in stockList:
    codename=codename.lower()
    fileName = 'c:\\stock\\data\\ts\\'+codename+'.csv'
    #print (fileName)
    df=ts.get_hist_data(codename)
    print (fileName,type(df))
    if df is not None:
    #reverse the DF sequence
        df = df.iloc[::-1]
        df['Adj Close']=df['close']
        df['Date']=df.index 
    #print(df.head(5))
    #print(stockList)        # 在控制台打印
        df = df.rename(columns={'date': 'Date', 'open': 'Open', 'high': 'High','low': 'Low','close':'Close','volume':'Volume'})
        df.to_csv(fileName, encoding='gbk')   # 保存到csv中
    #print (df.tail)
    else:
        pass
delta = datetime.now() - start
print("Program elapsed time in seconds", delta.seconds)