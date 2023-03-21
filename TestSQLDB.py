# !/usr/bin/env python
# coding=utf-8
import sys
import pandas as pd
import sqlite3

try:
    # 打开数据库连接
    db = sqlite3.connect('example.db')
except:
    print('Error when Connecting to DB.')
    sys.exit()
cursor = db.cursor()
cursor.execute("select * from stockinfo")
# 获取所有的数据，但不包含列表名
result = cursor.fetchall()
cols = cursor.description       # 返回列表头信息
print(cols)
col = []
# 依次把每个cols元素中的第一个值放入col数组
for index in cols:
    col.append(index[0])
result = list(result)   # 转成列表，方便存入DataFrame
result = pd.DataFrame(result, columns=col)
print(result)           # 输出结果
# 关闭游标和连接对象，否则会造成资源无法释放
cursor.close()
db.close()
