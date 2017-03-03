# -*- coding: utf-8 -*-
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
import time
currentdate = time.strftime("%Y-%m-%d", time.localtime())

# 发件人姓名列表
names = ['LiuYun', 'HuangShuo', 'LiJinSheng','WeiSui']

# 物流公司列表
kuaidiNames = ['shentong','zhongtong','shunfeng','yousu','youzhengguonei','yuantong']

# 统计当日发件数
def CurrentDayData(dbDir,tableName):

    db = create_engine(dbDir)
    metadata = MetaData(db)
    Session = sessionmaker(bind=db)
    session = Session()
    csvtable = Table(tableName, metadata, autoload=True)
    for name in names:
        count = session.query(csvtable).filter(and_(csvtable.c.DATE==currentdate,csvtable.c.NAME == name)).count()
        print name,"今天发件数为：",count
    session.close()

'''
    eng = create_engine(dbDir)
    conn = eng.connect()
    cursor = conn.execute("SELECT * from " + tableName + " WHERE DATE = ?", time.strftime("%Y-%m-%d", time.localtime()))
    x = 0
    for row in cursor:  # 如果有记录，则显示信息
        x = x + 1
        # print '[', x, ']', row[1], row[2], row[3], row[4]
    if x == 0:  # 如果无记录，则x = 0.
        print "无记录。"
    else:
        print "今天共发",x,"个。"
    conn.close()
'''

def isInDB(databaseAbsoluteRoute,tableName):  # 查询某个数据是否在数据库中。参数1位数据库路径，参数2为某个数据
    oneDanhao = raw_input('请输入要查询的单号：')
    db = create_engine(databaseAbsoluteRoute)
    metadata = MetaData(db)
    Session = sessionmaker(bind=db)
    session = Session()
    csvtable = Table(tableName, metadata, autoload=True)
    allDanhao = session.query(csvtable).filter(csvtable.c.DANHAO == oneDanhao).all()
    session.close()
    print allDanhao
    if allDanhao == []:
        print "无记录。"
    else:
        for danhao in allDanhao:
            print danhao[1],danhao[2],danhao[3],danhao[4]

'''
    eng = create_engine(databaseAbsoluteRoute)
    conn = eng.connect()
    cursor = conn.execute("SELECT * from "+ tableName + " WHERE DANHAO = ?", oneDanhao)  #通过？传入参数
    x = 0
    for row in cursor:   # 如果有记录，则显示信息
        x = x + 1
        print '[',x,']',row[1],row[2],row[3],row[4]
    if x == 0 :     # 如果无记录，则x = 0.
        print "无记录。"
    conn.close()
'''

def DBAnalysis(databaseAbsoluteRoute,tableName):  # 参数为数据库绝对路径
    db = create_engine(databaseAbsoluteRoute)
    metadata = MetaData(db)
    Session = sessionmaker(bind=db)
    session = Session()
    csvtable = Table(tableName, metadata, autoload=True)

    allCount = session.query(csvtable).count()
    print "本月总发件数为：",allCount

    # 统计该月各快递发件数
    for kuaidi in kuaidiNames:
        count = session.query(csvtable).filter(csvtable.c.WULIU == kuaidi).count()
        print kuaidi, "本月总件数为：", count

    for name in names:
        print "............................................"
        count = session.query(csvtable).filter(csvtable.c.NAME == name).count()
        print name,"本月总发件数为：",count
        for kuaidi in kuaidiNames:
            count = session.query(csvtable).filter(
                and_(csvtable.c.NAME == name, csvtable.c.WULIU == kuaidi)).count()
            print "本月",name,"发",kuaidi,count,"件"
    session.close()

'''
    eng = create_engine(databaseAbsoluteRoute)
    conn = eng.connect()
    cursor = conn.execute("SELECT NAME,DANHAO,WULIU from "+tableName)
    zt = st = yz = sf = yt = ys = yd = 0  # ZT中通,ST申通,YZ邮政,SF顺丰,YT圆通,YS优速,YD韵达
    LiuYun = 0 # 刘云
    LiJinSheng = 0 # 李金生
    WeiSui = 0 # 韦随
    HuangShuo = 0 # 黄硕
    lyzt = lyst = lyyz = lysf = lyyt = lyys = lyyd = 0  # 刘云中通等
    hszt = hsst = hsyz = hssf = hsyt = hsys = hsyd = 0  # 黄硕中通等
    wszt = wsst = wsyz = wssf = wsyt = wsys = wsyd = 0  # 韦随中通等
    ljszt = ljsst = ljsyz = ljssf = ljsyt = ljsys = ljsyd = 0 # 李金生中通等
    for row in cursor:
        if row[2] == 'zhongtong':  # 中通快递数量
            zt = zt + 1
        if row[2] == 'shentong':  # 申通快递数量
            st = st + 1
        if row[2] == 'youzhengguonei':  # 邮政快递数量
            yz = yz + 1
        if row[2] == 'shunfeng':  # 顺丰快递数量
            sf = sf +1
        if row[2] == 'yunda':  # 韵达快递数量
            yd = yd +1
        if row[2] == 'yuantong':  # 圆通快递数量
            yt = yt +1
        if row[2] == 'yousu':  # 优速快递数量
            ys = ys +1
        if row[0] == 'LiuYun':  # 刘云快递数量
            LiuYun = LiuYun +1
        if row[0] == 'LiJinSheng':  # 李金生快递数量
            LiJinSheng = LiJinSheng +1
        if row[0] == 'WeiSui':  # 韦随快递数量
            WeiSui = WeiSui +1
        if row[0] == 'HuangShuo' or row[0] == 'Huangshuo':  # 黄硕快递数量
            HuangShuo = HuangShuo +1
        # 刘云数据统计
        if row[0] == 'LiuYun' and row[2] == 'zhongtong':
            lyzt = lyzt + 1
        if row[0] == 'LiuYun' and row[2] == 'shentong':
            lyst = lyst + 1
        if row[0] == 'LiuYun' and row[2] == 'youzhengguonei':
            lyyz = lyyz + 1
        if row[0] == 'LiuYun' and row[2] == 'shunfeng':
            lysf = lysf + 1
        if row[0] == 'LiuYun' and row[2] == 'yunda':
            lyyd = lyyd + 1
        if row[0] == 'LiuYun' and row[2] == 'yuantong':
            lyyt = lyyt +1
        if row[0] == 'LiuYun' and row[2] == 'yousu':
            lyys = lyys + 1
        # 黄硕数据统计
        if row[0] == 'HuangShuo' and row[2] == 'zhongtong':
            hszt = hszt + 1
        if row[0] == 'HuangShuo' and row[2] == 'shentong':
            hsst = hsst + 1
        if row[0] == 'HuangShuo' and row[2] == 'youzhengguonei':
            hsyz = hsyz + 1
        if row[0] == 'HuangShuo' and row[2] == 'shunfeng':
            hssf = hssf + 1
        if row[0] == 'HuangShuo' and row[2] == 'yunda':
            hsyd = hsyd + 1
        if row[0] == 'HuangShuo' and row[2] == 'yuantong':
            hsyt = hsyt +1
        if row[0] == 'HuangShuo' and row[2] == 'yousu':
            hsys = hsys + 1
        # 韦随数据统计
        if row[0] == 'WeiSui' and row[2] == 'zhongtong':
            wszt = wszt + 1
        if row[0] == 'WeiSui' and row[2] == 'shentong':
            wsst = wsst + 1
        if row[0] == 'WeiSui' and row[2] == 'youzhengguonei':
            wsyz = wsyz + 1
        if row[0] == 'WeiSui' and row[2] == 'shunfeng':
            wssf = wssf + 1
        if row[0] == 'WeiSui' and row[2] == 'yunda':
            wsyd = wsyd + 1
        if row[0] == 'WeiSui' and row[2] == 'yuantong':
            wsyt = wsyt +1
        if row[0] == 'WeiSui' and row[2] == 'yousu':
            wsys = wsys + 1
        # 李金生数据统计
        if row[0] == 'LiJinSheng' and row[2] == 'zhongtong':
            ljszt = ljszt + 1
        if row[0] == 'LiJinSheng' and row[2] == 'shentong':
            ljsst = ljsst + 1
        if row[0] == 'LiJinSheng' and row[2] == 'youzhengguonei':
            ljsyz = ljsyz + 1
        if row[0] == 'LiJinSheng' and row[2] == 'shunfeng':
            ljssf = ljssf + 1
        if row[0] == 'LiJinSheng' and row[2] == 'yunda':
            ljsyd = ljsyd + 1
        if row[0] == 'LiJinSheng' and row[2] == 'yuantong':
            ljsyt = ljsyt +1
        if row[0] == 'LiJinSheng' and row[2] == 'yousu':
            ljsys = ljsys + 1



    print "本月数据统计："
    print "黄硕[", "中通",hszt,"申通",hsst,"优速",hsys,"邮政",hsyz,"]合计",hszt+hsst+hsys+hsyz,"件"
    print "刘云[", "中通",lyzt,"申通",lyst,"优速",lyys,"邮政",lyyz,"]合计",lyzt+lyst+lyys+lyyz+lyyt+lysf,"件"
    print "李金生[", "中通",ljszt,"申通",ljsst,"优速",ljsys,"邮政",lyyz,"]合计",ljszt+ljsst+ljsys+ljsyz,"件"
    print "韦随[", "中通",wszt,"申通",wsst,"优速",wsys,"邮政",wsyz,"]合计",wszt+wsst+wsys+wsyz,"件"

    print "合计",HuangShuo+LiJinSheng+LiuYun+WeiSui,"件。"

    if zt > 0:
        print "中通快递一共有", zt, "个。"
    if st > 0:
        print "申通快递一共有", st, "个。"
    if yz > 0:
        print "邮政快递一共有", yz, "个。"
    if sf > 0:
        print "顺丰快递一共有", sf, "个。"
    if yt > 0:
        print "圆通快递一共有", yt, "个。"
    if yd > 0:
        print "韵达快递一共有", yd, "个。"
    if ys > 0:
        print "优速快递一共有", ys, "个。"

    print "合计", zt+st+yz+sf+yt+yd+ys, "个。"
    conn.close()
'''