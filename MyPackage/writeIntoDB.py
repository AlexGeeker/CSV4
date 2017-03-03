# -*- coding: utf-8 -*-

import csv
import sqlite3
import json
import urllib2
import os
import os.path
import time
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


# 识别快递单号
def getKD(DanHao):
    response = urllib2.urlopen("http://www.kuaidi100.com/autonumber/auto?num="+DanHao).read().decode('utf-8')
    if response == '[]':
        return '0'
    else:
        responseJson = json.loads(response)
        return responseJson[0]["comCode"]

# 写入数据库
def WriteIntoDB(dbDir,tableName,name,danhao,wuliu):
    # 链接数据库
    db = create_engine(dbDir)
    metadata = MetaData(db)
    csvtable = Table(tableName, metadata, autoload=True)
    i = csvtable.insert()
    i.execute(NAME=name, DANHAO=danhao, WULIU=wuliu,DATE=time.strftime("%Y-%m-%d", time.localtime()))
    #    conn = eng.connect()
#    conn.execute("insert into " + tableName + "(NAME,DANHAO,WULIU) values ('%s','%s','%s')" %(name,danhao,wuliu))

 #   conn = sqlite3.connect('mycsv.db')
 #   cursor = conn.cursor()
 #   cursor.execute("insert into CSV4 (NAME,DANHAO,WULIU) values ('%s','%s','%s')" %(name,danhao,wuliu));
    db.dispose()
    print name+u"所发快递单号为："+danhao+":"+wuliu+u"已记录";
#    conn.commit()  # 提交数据
#    db.close()  # 关闭数据库


# 打开文件，并调用函数WriteIntoDB
def WriteCsvToDB(dbDir,tableName,CsvFileName):  # 参数为CSV文件名和绝对路径
    with open(CsvFileName) as csvFile:
        dictreader = csv.DictReader(csvFile)

        print dictreader.fieldnames
        i = 0
        TM = u'条码'
        for line in dictreader:
            if 'HS'in CsvFileName:
                WriteIntoDB(dbDir,tableName,'HuangShuo',line['\xcc\xf5\xc2\xeb'],getKD(line['\xcc\xf5\xc2\xeb']))
            elif 'LY' in CsvFileName:
                WriteIntoDB(dbDir,tableName,'LiuYun', line['\xcc\xf5\xc2\xeb'], getKD(line['\xcc\xf5\xc2\xeb']))
            elif 'LJS'in CsvFileName:
                WriteIntoDB(dbDir,tableName,'LiJinSheng', line['\xcc\xf5\xc2\xeb'], getKD(line['\xcc\xf5\xc2\xeb']))
            elif 'WS' in CsvFileName:
                WriteIntoDB(dbDir,tableName,'WeiSui', line['\xcc\xf5\xc2\xeb'], getKD(line['\xcc\xf5\xc2\xeb']))
            else:
                print u"文件名错误！"
                return u"文件名错误！"
    #        print line['\xcc\xf5\xc2\xeb']+getKD(line['\xcc\xf5\xc2\xeb'])
            i = i+1
        print u"条码总数为：",i
        return i

        print "Records created successfully"

# 遍历目录，寻找全部csv文件，并调用数据库写入函数
def findAllCSVtoWrite(csvDir,dbDir,tableName):
    i = 0
    for parent,dirnames,filenames in os.walk(csvDir):  # 遍历目录并调用数据库写入函数
        i = i +1
        for filename in filenames:
            if '.csv' in filename:
                WriteCsvToDB(dbDir,tableName,os.path.join(parent,filename))
    if i == 0:
        print "提示：指定目录未发现csv文件。"

# 使用sqlalchemy 语法创建table
def createTable(dbDir,tableName):

    db = create_engine(dbDir)
    db.echo = False
    metadata = MetaData(db)
    csv = Table(tableName, metadata,
                Column('ID', Integer, primary_key=True,autoincrement=True),
                Column('NAME', TEXT,nullable=False),
                Column('DANHAO', TEXT,nullable=False),
                Column('WULIU', TEXT,nullable=False),
#                Column(u'timestamp', TIMESTAMP(timezone=True), primary_key=False, nullable=False, default=time_now),
                Column('DATE',TEXT),
                )
    csv.create()
    print "数据表",tableName,"创建成功。"

# 删除一个table
def deleteTable(dbDir,tableNametoDelete):
    db = create_engine(dbDir)
    metadata = MetaData(db)

    csvtable = Table(tableNametoDelete, metadata, autoload=True)
    csvtable.drop(db)
    print "成功删除表;",tableNametoDelete

    # 链接数据库，创建table（老方法）
#def createTable():
#    conn = sqlite3.connect('mycsv.db')
#    print "Opened database successfully";

 #   conn.execute('''create table kdtj201702
 #           (ID INTEGER PRIMARY KEY AUTOINCREMENT NULL,
#            NAME TEXT NOT NULL,
#            DANHAO TEXT NOT NULL UNIQUE,
#            WULIU TEXT NOT NULL,
#            Timestamp DATETIME DEFAULT (datetime('now','localtime')));''')

#    print "Table created successfully";

#    conn.close()

# 使用sqlalchemy 创建表table
#def createTable(dbDir,tableName):
#    eng = create_engine(dbDir)
#    conn = eng.connect()
#    conn.execute('''CREATE TABLE IF NOT EXISTS '''+ tableName + '''
#                 (ID INTEGER PRIMARY KEY AUTOINCREMENT NULL,
#                 NAME TEXT NOT NULL,
#                 DANHAO TEXT NOT NULL UNIQUE,
#                 WULIU TEXT NOT NULL,
#                 Timestamp DATETIME DEFAULT (datetime('now','localtime')))''')
#
#    conn.close()  # 关闭数据库
#    print "数据表",tableName,"创建成功。"

# 删除某些记录
def deleteRow(dbDir,tableName,date):
    db = create_engine(dbDir)
    metadata = MetaData(db)
    Session = sessionmaker(bind=db)
    session = Session()
    csvtable = Table(tableName, metadata, autoload=True)
    count = session.query(csvtable).filter(csvtable.c.DATE == date).count()
    session.query(csvtable).filter(csvtable.c.DATE == date).delete(synchronize_session=False)
    session.commit()
    session.close()
    print "已删除信息",count,"条"

# 判断CSV文件中的所有单号是否存在于数据库中
def CsvIsInDB(dbDir,tableName,csvfile):
    # 链接数据库
    db = create_engine(dbDir)
    metadata = MetaData(db)
    Session = sessionmaker(bind=db)
    session = Session()
    csvtable = Table(tableName, metadata, autoload=True)
    # 打开csv文档
    with open(csvfile) as csvFile:
        dictreader = csv.DictReader(csvFile)
        countcsv = 0
        for line in dictreader:
            if session.query(csvtable).filter(csvtable.c.DANHAO == line['\xcc\xf5\xc2\xeb']).count()>0:
                countcsv = countcsv +1
        session.close()
    if countcsv >= 3:
        return True
    else:
        return False
