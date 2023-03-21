# !/usr/bin/env python
# coding=utf-8
import pandas as pd
import numpy as np
import math,sys
import sqlite3
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from tslib import *

workFolder = "c:\\stock\export\\stock\\"
dataBaseFolder = 'c:\\stock\\'
dataBaseName = 'stock.db'

def getStockData(code, dataBaseName):
    try:
        # 打开数据库连接
        db = sqlite3.connect(dataBaseName)
    except:
        print('Error when Connecting to DB.')
        sys.exit()
    cursor = db.cursor()
    cursor.execute('select * from stock_'+code)
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
# 本次直接从文件中读取数据
#df = pd.read_csv('c:/stock/export/STOCK/SH601318.csv',skiprows=[0,1],names=("Date","Open","High","Low","Close","Volume","vol2"), encoding='gbk')
# delete the last colume


# 从文件中获取数据
#origDf = pd.read_csv('c:/stock/data/6035052018-09-012019-05-31.csv',encoding='gbk')
origDf = getStockData('SH600000', dataBaseName)
MA_5 = calMA(origDf, 5)
MA_13 = calMA(origDf, 13)
MA_55 = calMA(origDf, 55)
MA_89 = calMA(origDf, 89)
MA_120 = calMA(origDf, 120)
MA_250 = calMA(origDf, 250)
MA_500 = calMA(origDf, 500)

df = origDf[['close', 'MA_5', 'MA_13','MA_55' ,'MA_120']].dropna()

#print (df.tail(5))
featureData = df[['MA_5', 'MA_13', 'MA_55','MA_120']].dropna()
#print (featureData)
# 划分特征值和目标值
feature = featureData.values
target = np.array(df['close'])

# 划分训练集，测试集
feature_train, feature_test, target_train ,target_test = train_test_split(feature,target,test_size=0.5)
pridectedDays = int(math.ceil(0.1 * len(origDf)))  # 预测天数
lrTool = LinearRegression()
lrTool.fit(feature_train,target_train)              # 训练
print(lrTool.score(feature_train,target_train))
# 用测试集预测结果
predictByTest = lrTool.predict(feature_test)
# 组装数据
index=0
# 在前95%的交易日中，预测结果和收盘价一致
while index < len(origDf) - pridectedDays:    
    df.loc[index,'predictedVal']=origDf.loc[index,'close']
    df.loc[index,'date']=origDf.loc[index,'date']
    index = index+1
predictedCnt=0
# 在后5%的交易日中，用测试集推算预测股价    
while predictedCnt<pridectedDays:
    df.loc[index,'predictedVal']=predictByTest[predictedCnt]
    df.loc[index,'date']=origDf.loc[index,'date']
    predictedCnt=predictedCnt+1
    index=index+1

plt.figure()
df['predictedVal'].plot(color="red",label='predicted Data')
df['close'].plot(color="blue",label='Real Data')
plt.legend(loc='best')      # 绘制图例
# 设置x坐标的标签
major_index=df.index[df.index%10==0]
major_xtics=df['date'][df.index%10==0]
plt.xticks(major_index,major_xtics)
plt.setp(plt.gca().get_xticklabels(), rotation=30) 
# 带网格线，且设置了网格样式
plt.grid(linestyle='-.')
plt.show()