# coding=utf-8
import sqlite3
import pandas as pd
import os
import datetime
from datetime import datetime

workFolder = "data\\us\\"
dataBaseFolder = 'c:\\stock\\'
dataBaseName = 'us_stock.db'
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
                #print(filename)
                db = pd.read_csv(workFolder+filename, skiprows=[0], names=(
                    "date", "open", "high", "low", "close", "adj close", "volume"), encoding="gbk", header=None)
                #db.drop([len(db)-1], inplace=True) //delete the last row of the db
                stockcode = filename[0:-4]
                print (stockcode)
                db.to_sql("stock_"+stockcode, connection, if_exists="replace")
                connection.commit()
    connection.close()

getSockDataFromDB(workFolder, dataBaseFolder, dataBaseName)
delta = datetime.now() - start
print("file transfer elapsed time in seconds", delta.seconds)