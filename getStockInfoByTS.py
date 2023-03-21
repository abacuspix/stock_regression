# coding=utf-8
import tushare as ts
from tslib import *
import time

dataBaseName = 'c:\\stock\\stock.db'
#dataBaseName = 'c:\\stock\\etf.db'
t = time.time()
start = datetime.now()
print (start)
stockList = getAllStockList(dataBaseName)
#print (stockList)

for codename in stockList:
    codename=codename.lower()
    fileName = 'c:\\stock\\data\\ts\\'+codename+'.csv'
    #print (fileName)
    df=ts.get_hist_data(codename)
    print(codename,type(df)) 
    #reverse the DF sequence
    if df is not None:
        df = df.iloc[::-1]
        df['Adj Close']=df['close']
        df['Date']=df.index 
        #print(df.head(5))
        #print(codename)        # 在控制台打印
        df = df.rename(columns={'date': 'Date', 'open': 'Open', 'high': 'High','low': 'Low','close':'Close','volume':'Volume'})
        df.to_csv(fileName, encoding='gbk')   # 保存到csv中
    else:
        pass
        #print (df.tail)
delta = datetime.now() - start
print("Program elapsed time in seconds", delta.seconds)