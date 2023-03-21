# !/usr/bin/env python
# coding=utf-8
import sys
import sqlite3

try:
    # 打开数据库连接    
    db = sqlite3.connect('stock1.db')
except:
    print('Error when Connecting to DB.')
    sys.exit()
cursor = db.cursor()
# 插入一条记录
insertSql = "insert into stockinfo (date,open,close,high,low,vol,stockCode ) values ('20190103',16.65,15.31,15.78,16.24,94733382,'600895')"
cursor.execute(insertSql)
db.commit()     # 需要调用commit方法才能把操作提交到数据表中使之生效
# 删除一条记录
deleteSql = "delete from stockinfo where stockCode = '600895' and date='20190103'"
cursor.execute(deleteSql)
db.commit()
# 更新数据
insertErrorSql = "insert into stockinfo (date,open,close,high,low,vol,stockCode ) values ('201901030000',16.65,15.31,15.78,16.24,94733382,'600895')"
cursor.execute(insertErrorSql)  # 插入了一条错误的记录，date不对
db.commit()
updateSql = "update stockinfo set date='20190103' where date='201901030000' and stockCode = '600895'"
cursor.execute(updateSql)
db.commit()
cursor.close()
db.close()
