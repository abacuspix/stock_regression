""" # coding=utf-8
import pandas_datareader
stockCodeList = []
#stockCodeList.append('600007.ss')  # 沪股“中国国贸”
#stockCodeList.append('000001.sz')  # 深股“平安银行”
#stockCodeList.append('2318.hk')    # 港股“中国平安”
stockCodeList.append('IBM')         # 美股，JNPR，直接输入股票代码不带后缀   
stockCodeList.append('TQQQ')        # 美股，JNPR，直接输入股票代码不带后缀
stockCodeList.append('SQQQ')  
for code in stockCodeList:
    # 为了演示，只取一天的交易数据

    stock = pandas_datareader.get_data_yahoo(code, '1970-01-02', '2022-01-02')
    print(stock.head(5)) """
import datetime as dt
import yfinance as yf
import datetime
import time
import pandas as pd
from datetime import datetime
import csv


start = datetime.now()
print (start)
def getCodeFromYahooList():
    with open('c:\\stock\\inxYahoo.csv', 'r') as file:
        reader = csv.reader(file)
        stockList=[]
        for row in reader:
            stockList.append(row[0])
    return stockList

# db = pd.read_csv("c:\\stock\\nasdaq_screener.csv" )
# print (db.head(5))
# stockList=db['Symbol']
start = dt.datetime(2010,1,1)
#end = dt.datetime(2019,12,31)
end = datetime.now()
stockList=getCodeFromYahooList()
for codename in stockList:
    print (codename)
    df = yf.download(codename, start , end, adjusted=True)
    #print (data.tail(5))
    #df = df.rename(columns={'Date': 'date', 'Open': 'open', 'High': 'high','Low': 'low','Close':'close',
                            #'Adj Close':'adj close','Volume':'volume'})
    #Date,Open,High,Low,Close,Adj Close,Volume
    #print(df.size)
    fileName = 'c:\\stock\\data\\us\\'+codename+'.csv'
    if (df.size>20):
        df.to_csv(fileName, encoding='gbk')
        newcodename=codename
        with open('c:\\stock\\inxYahoo-new.csv', 'a') as file:
            file.write(newcodename+"\n")
delta = datetime.now() - start
print("Program elapsed time in seconds", delta.seconds)