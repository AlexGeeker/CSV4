# -*- coding: utf-8 -*-

from MyPackage import dbfenxi
from MyPackage import writeIntoDB
import time
from datetime import date,timedelta
import datetime

#dbDir = "sqlite:///C:/Users/Administrator/PycharmProjects/CSV/KDTJ.db"
csvDir = "D:\KDdata\\201702"
#tableName = 'CSV'+time.strftime("%Y-%m-%d", time.localtime())
#tableName = 'KDTJ201702'

# 需要删除的table名
#tableNametoDelete = 'KDTJ201701'

# 创建数据表 说明：仅需要时打开。
#writeIntoDB.createTable(dbDir,tableName)

# 将全部csv文件写入数据库（需要使用时打开，否则会重复写入）
#writeIntoDB.findAllCSVtoWrite(csvDir,dbDir,tableName)  # 参数1位csv文件目录，参数2位数据库所在目录，参数3为表名

# 数据库数据统计分析
#dbfenxi.DBAnalysis(dbDir,tableName)  # 参数1为数据库目录，参数2为表名

# 从数据库中查找某个记录
#dbfenxi.isInDB(dbDir,tableName)  # 参数1为数据库目录，参数2为表名

# 统计当天数据
#dbfenxi.CurrentDayData(dbDir,tableName)

# 删除某个table
#writeIntoDB.deleteTable(dbDir,tableNametoDelete)

# 删除某些记录 （可根据时间，姓名，物流信息等删除某些记录）
#writeIntoDB.deleteRow(dbDir,tableName,'201702')
a = [(1,2,3),(4,5,6)]
b = [(7,8,9),(10,11,12)]
print a+b

yesterday = date.today() - timedelta(1)
preyesterday = date.today() - timedelta(2)
print yesterday
print preyesterday