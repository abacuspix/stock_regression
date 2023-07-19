import datetime as dt
import yfinance as yf
import datetime
import time
from tslib import *
from datetime import datetime
import csv

dataBaseName = 'c:\\stock\\cn_stock.db'
start = datetime.now()
print (start)

stockList = getAllStockList(dataBaseName)
#print (stockList)
start = dt.datetime(2010,1,1)
end = datetime.now()
#df = yf.download("002108.SZ", start , end)
#print (df.head(5))
def getStock():
    for codename in stockList:
        stockname=codename[6:]
        codename=codename[6:]
        print(codename)
        if codename.startswith("6"):
           codename=codename+".ss"
        elif codename.startswith("3"):
           codename=codename+".sz"
        elif codename.startswith("0"): 
            codename=codename+".sz"   
        elif codename.startswith("5"): 
            codename=codename+".ss"   
        else: 
            continue
    #codename=codename[2:].lower()+".ss"
        df = yf.download(codename, start , end, adjusted=True)
    #print (data.tail(5))
    #df = df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high','Low': 'low','Close':'close',
                            #'Adj Close':'adj close','Volume':'volume'})
    #Date,Open,High,Low,Close,Adj Close,Volume
        fileName = 'c:\\stock\\data\\cn\\'+stockname+'.csv'
        if (df.size>20):
            df.to_csv(fileName, encoding='gbk')
getStock()
delta = datetime.now() - start
print("Program elapsed time in seconds", delta.seconds)