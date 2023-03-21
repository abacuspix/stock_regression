# !/usr/bin/env python
# coding=utf-8
import pandas as pd
from tslib import PPSR

# 从文件中读取数据
df = pd.read_csv('c:/stock/export/STOCK/SH601318.csv',skiprows=[0,1],names=("date","open","high","low","close","volume","vol2"), encoding='gbk')
#delete the last colume
df.drop([len(df)-1],inplace=True)

#data=OBV(df,5)
#print (data.tail(5))

t=PPSR(df)
print (t.tail(5))
