import datetime as dt
import yfinance as yf
import datetime
import time
from tslib import *
from datetime import datetime
import csv

dataBaseName = 'c:\\stock\\stock.db'
start = datetime.now()
print (start)

stockList = getAllStockList(dataBaseName)
#print (stockList)
start = dt.datetime(2020,1,1)
end = datetime.now()
#df = yf.download("002108.SZ", start , end)
#print (df.head(5))
def getStock():
    for codename in stockList:
        stockname=codename[2:]
        codename=codename[2:]
        if codename.startswith("6"):
           codename=codename+".ss"
        elif codename.startswith("3"):
           codename=codename+".sz"
        elif codename.startswith("0"): 
            codename=codename+".sz"   
    #codename=codename[2:].lower()+".ss"
        df = yf.download(codename, start , end, adjusted=True)
    #print (data.tail(5))
    #df = df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high','Low': 'low','Close':'close',
                            #'Adj Close':'adj close','Volume':'volume'})
    #Date,Open,High,Low,Close,Adj Close,Volume
        fileName = 'c:\\stock\\data\\cn\\'+stockname+'.csv'
        df.to_csv(fileName, encoding='gbk')
getStock()
delta = datetime.now() - start
print("Program elapsed time in seconds", delta.seconds)