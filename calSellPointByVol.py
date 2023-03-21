# !/usr/bin/env python
# coding=utf-8
import pandas_datareader
import pandas as pd
import numpy as np
# 涨幅是否大于指定比率


def isMoreThanPer(lessVal, highVal, per):
    if np.abs(highVal-lessVal)/lessVal > per/100:
        return True
    else:
        return False
# 涨幅是否小于指定比率


def isLessThanPer(lessVal, highVal, per):
    if np.abs(highVal-lessVal)/lessVal < per/100:
        return True
    else:
        return False


# 本次直接从文件中读取数据
df = pd.read_csv('c:/stock/export/STOCK/SH601318.csv', skiprows=[0, 1], names=(
    "Date", "Open", "High", "Low", "Close", "Volume", "vol2"), encoding='gbk')
# delete the last colume
df.drop([len(df)-1], inplace=True)
cnt = 0
while cnt <= len(df)-1:
    try:
        # 规则1：连续三天收盘价变动不超过3%
        if isLessThanPer(df.iloc[cnt]['Close'], df.iloc[cnt+1]['Close'], 3) and isLessThanPer(df.iloc[cnt]['Close'], df.iloc[cnt+2]['Close'], 3):
            # 规则2：连续三天成交量跌幅超过75%
            if isMoreThanPer(df.iloc[cnt+1]['Volume'], df.iloc[cnt]['Volume'], 75) and isMoreThanPer(df.iloc[cnt+2]['Volume'], df.iloc[cnt]['Volume'], 75):
                print("Sell Point on:" + df.iloc[cnt]['Date'])
    except:
        pass
    cnt = cnt+1
