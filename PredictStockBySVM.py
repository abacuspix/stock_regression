# !/usr/bin/env python
# coding=utf-8
import pandas as pd
from sklearn import svm, preprocessing
import matplotlib.pyplot as plt
import sys,sqlite3
from tslib import *

workFolder = "c:\\stock\export\\stock\\"
dataBaseFolder = 'c:\\stock\\'
dataBaseName = 'stock.db'

#origDf = pd.read_csv('c:/stock/data/6035052018-09-012019-05-31.csv', encoding='gbk')

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
origDf = getStockData('SH600000', dataBaseName)
df = origDf[['close', 'high', 'low', 'open', 'volume', 'date']]
# diff列表示本日和上日收盘价的差
df['diff'] = df["close"]-df["close"].shift(1)
df['diff'].fillna(0, inplace=True)
# up列表示本日是否上涨，1表示涨，0表示跌
df['up'] = df['diff']
df['up'][df['diff'] > 0] = 1
df['up'][df['diff'] <= 0] = 0
# 预测值暂且初始化为0
df['predictForUp'] = 0

# 目标值是真实的涨跌情况
target = df['up']

length = len(df)
trainNum = int(length*0.8)
predictNum = length-trainNum
# 选择指定列作为特征列

#print (df.head(5))
#feature = df[['MA_5', 'MA_13', 'MA_55', 'MA_120', 'volume']]
feature = df[['close', 'high', 'low', 'open', 'volume']]
# 标准化处理特征值
feature = preprocessing.scale(feature)

# 训练集的特征值和目标值
featureTrain = feature[0:trainNum]
targetTrain = target[0:trainNum]
svmTool = svm.SVC(kernel='linear')
svmTool.fit(featureTrain, targetTrain)

print(svmTool.score(featureTrain, targetTrain))

predictedIndex = trainNum
# 逐行预测测试集
while predictedIndex < length:
    testFeature = feature[predictedIndex:predictedIndex+1]
    predictForUp = svmTool.predict(testFeature)
    df.loc[predictedIndex, 'predictForUp'] = predictForUp
    predictedIndex = predictedIndex+1

# 该对象只包含预测数据，即只包含测试集
dfWithPredicted = df[trainNum:length]

# 开始绘图，创建两个子图
figure = plt.figure()
# 创建子图
(axClose, axUpOrDown) = figure.subplots(2, sharex=True)
dfWithPredicted['close'].plot(ax=axClose)
dfWithPredicted['predictForUp'].plot(
    ax=axUpOrDown, color="red", label='Predicted Data')
dfWithPredicted['up'].plot(ax=axUpOrDown, color="blue", label='Real Data')
plt.legend(loc='best')      # 绘制图例

# 设置x轴坐标的标签和旋转角度
major_index = dfWithPredicted.index[dfWithPredicted.index % 2 == 0]
major_xtics = dfWithPredicted['date'][dfWithPredicted.index % 2 == 0]
# plt.xticks(major_index, major_xtics)
# plt.setp(plt.gca().get_xticklabels(), rotation=30)
# plt.title("通过SVM预测stock的涨跌情况")
# plt.rcParams['font.sans-serif'] = ['SimHei']
# plt.show()
