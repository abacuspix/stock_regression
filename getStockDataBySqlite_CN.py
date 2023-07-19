# coding=utf-8
import sqlite3
import pandas as pd
import os
import datetime
from datetime import datetime

workFolder = "data\\cn\\"
dataBaseFolder = 'c:\\stock\\'
dataBaseName = 'cn_stock.db'
start = datetime.now()

def getSockDataFromDB(workFolder, dataBaseFolder, dataBaseName):
    # create connection
    connection = sqlite3.connect(dataBaseFolder+dataBaseName)
    for filename in os.listdir(workFolder):
        size = os.path.getsize(workFolder+filename)
        if size < 500:
            pass
        else:
            if filename.endswith(".csv"):
                # Prints only text file present in My Folder
                print(filename)
                db = pd.read_csv(workFolder+filename, skiprows=[0], 
                                 names=("date", "open", "high", "low", "close", "volume", "value"), encoding="gbk", header=None)
                #db.drop([len(db)-1], inplace=True)
                stockcode = filename[0:-4]
                db.to_sql("stock_"+stockcode, connection, if_exists="replace")
                connection.commit()
    connection.close()

getSockDataFromDB(workFolder, dataBaseFolder, dataBaseName)
delta = datetime.now() - start
print("file transfer elapsed time in seconds", delta.seconds)