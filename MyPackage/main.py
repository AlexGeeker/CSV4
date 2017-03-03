# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,func,distinct
from record import Record,Base,Last_Month_Record
import urllib2
import json
import time,datetime
from datetime import date,timedelta

currentMonth = time.strftime("%Y%m", time.localtime())

today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lastMonthTable = lastMonth.strftime("%Y%m")

# 昨天的日期
yesterday = date.today() - timedelta(1)
# 发件人姓名列表
names = ['LiuYun', 'HuangShuo', 'LiJinSheng','WeiSui']
# 物流公司列表
kuaidiNames = ['shentong','zhongtong','shunfeng','yousu','youzhengguonei','yuantong']
# 当天日期
currentdate = time.strftime("%Y-%m-%d", time.localtime())

engine = create_engine("sqlite:///C:\Users\Administrator\PycharmProjects\CSV\KDTJ.db",echo=False)
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

# 识别快递单号
def getKD(DanHao = None):
    if DanHao == None:
        DanHao = raw_input('请输入要识别的单号：')
    response = urllib2.urlopen("http://www.kuaidi100.com/autonumber/auto?num="+DanHao).read().decode('utf-8')
    if response == '[]':
        print '尚无记录！'
        return '0'
    else:
        responseJson = json.loads(response)
        print responseJson[0]["comCode"]
        return responseJson[0]["comCode"]

# 添加一条记录
def add_one_record(name,danhao,date,wuliu='0'):
    new_record = None
    if date[0:4]+date[5:7] == lastMonthTable:
        new_record = Last_Month_Record(name, danhao.strip(), wuliu, date)
    elif date[0:4]+date[5:7] == currentMonth:
        new_record = Record(name, danhao.strip(), wuliu, date)
    session.add(new_record)
    session.commit()
    session.close()

# 查询一条记录
def find_one_record(danhao = None):
#    if danhao == None:
#        danhao = raw_input('请输入要查询的单号：')
    allDanhao = session.query(Record).filter(Record.DANHAO == danhao).all() + session.query(Last_Month_Record).filter(Last_Month_Record.DANHAO == danhao).all()
    print allDanhao
    session.close()
    if allDanhao == []:
        print "无记录。"
        return False
    else:
        i = 0
        danhaodict = []
        for danhao in allDanhao:
            print danhao.NAME,danhao.DANHAO,danhao.WULIU,danhao.DATE
            danhaodict.append([danhao.NAME,danhao.DANHAO,danhao.WULIU,danhao.DATE])
            i = i + 1
        return danhaodict

# 更新一条记录
def update_one_record(danhao = None):
    if danhao == None:
        danhao = raw_input('请输入需要更新的物流单号：')
    allDanhao = session.query(Record).filter(Record.DANHAO == danhao).all()
    if allDanhao == []:
        print "无记录。"
    else:
        wuliu = getKD(danhao)
        for x in allDanhao:
            session.query(Record).filter(Record.DANHAO == danhao).update({Record.WULIU:wuliu})
            print u'%s已更新为%s'% (danhao,wuliu)
    session.commit()
    session.close()

# 删除一条记录
def delete_one_record(danhao = None):
    if danhao == None:
        danhao = raw_input('请输入要删除的物流单号：')
    count = session.query(Record).filter(Record.DANHAO == danhao).count()
    session.query(Record).filter(Record.DANHAO == danhao).delete(synchronize_session=False)
    session.commit()
    print '需要删除的单号：%s,共删除%d条记录。' % (danhao,count)
    session.close()

# 统计所有人当天发件数
def everyone_today_count():
    count = {}
    for name in names:
        total = session.query(Record).filter(Record.DATE==currentdate,Record.NAME == name).count()
        count[name] = total
        print name,"今天发件数为：",total
    session.close()
    return count

# 统计所有人昨天发件数
def everyone_yesterday_count():
    count = {}
    for name in names:
        total = session.query(Record).filter(Record.DATE==yesterday,Record.NAME == name).count()
        count[name] = total
        print name,"昨天发件数为：",total
    session.close()
    return count

# 统计所有人本月发件数
def everyone_month_count():
    count = {}
    for name in names:
        total = session.query(Record).filter(Record.NAME == name).count()
        count[name] = total
        print name,"本月发件数为：",total
    session.close()
    print count
    return count

# 统计所有快递本月发件数
def wuliu_month_count():
    count = {}
    for kuaidi in kuaidiNames:
        total = session.query(Record).filter(Record.WULIU == kuaidi).count()
        count[kuaidi] = total
        print kuaidi,"本月发件数为：",total
    session.close()
    print count
    return count

# 统计本月快递总数
def all_wuliu_count():
    return session.query(Record).count()

# 上个月各人发件数
def everyone_last_month_count():
    count = {}
    for name in names:
        total = session.query(Last_Month_Record).filter(Last_Month_Record.NAME == name).count()
        count[name] = total
        print name,"上月发件数为：",total
    session.close()
    print count
    return count

# 上个月所有快递发件数
def wuliu_last_month_count():
    count = {}
    for kuaidi in kuaidiNames:
        total = session.query(Last_Month_Record).filter(Last_Month_Record.WULIU == kuaidi).count()
        count[kuaidi] = total
        print kuaidi,"上月发件数为：",total
    session.close()
    print count
    return count

# 根据单号更新物流信息（WULIU默认值为0）
def update_all_wuliu():
    updated = 0
    updated_lastmonth = 0
    # 更新本月
    all_wuliu = session.query(Record).filter(Record.WULIU == '0').all()
    x = 0
    for wuliu in all_wuliu:
        x = x + 1
        kuaidi = getKD(wuliu.DANHAO)
        session.query(Record).filter(Record.DANHAO == wuliu.DANHAO).update({Record.WULIU:kuaidi})
        print u'%s已更新为%s'% (wuliu.DANHAO,kuaidi)
        if x > 100:
            session.commit()
        updated = updated + 1
    # 更新上月
    last_month_wuliu = session.query(Last_Month_Record).filter(Last_Month_Record.WULIU == '0').all()
    y = 0
    for wuliu in last_month_wuliu:
        y = y + 1
        kuaidi = getKD(wuliu.DANHAO)
        session.query(Last_Month_Record).filter(Last_Month_Record.DANHAO == wuliu.DANHAO).update({Last_Month_Record.WULIU:kuaidi})
        print u'%s已更新为%s'% (wuliu.DANHAO,kuaidi)
        if y > 100:
            session.commit()
        updated_lastmonth = updated_lastmonth + 1

    session.close()
    return updated + updated_lastmonth

# 统计上个月每个人每日的发件数
def lastMonth_everyone_everyday_count(name):
    count = []
    # return session.query(Last_Month_Record).filter(Last_Month_Record.NAME == name).group_by(Last_Month_Record.DATE).count()
    #return session.query(Last_Month_Record.NAME).filter(Last_Month_Record.NAME == name).group_by(Last_Month_Record.DATE).count()
    # return session.query(func.count(Last_Month_Record.NAME), Last_Month_Record.NAME, Last_Month_Record.DATE).group_by(Last_Month_Record.DATE).all()
    # return session.query(func.count(Last_Month_Record.ID), Last_Month_Record.NAME).group_by(Last_Month_Record.NAME).all()    # 每人月度统计的正确方法
    #return session.query(func.count(distinct(Last_Month_Record.DATE)))
    for odate in session.query(distinct(Last_Month_Record.DATE)):
        count.append(([odate[0]],session.query(Last_Month_Record).filter(Last_Month_Record.NAME == name, Last_Month_Record.DATE == odate[0]).count()))
        #print odate[0],session.query(Last_Month_Record).filter(Last_Month_Record.NAME == name, Last_Month_Record.DATE == odate[0]).count()
        #print odate[0]
    return count
    #return session.query(Last_Month_Record.DATE).all()


if __name__ == '__main__':
    print '1:添加一条记录'
    print '2:查找一个单号'
    print '3:更新一条记录'
    print '4:识别一个单号'
    print '5:删除一个单号'
    print '6:统计今天发件数'
    print '7:统计本月所有人发件数'
    print '8:统计本月所有快递发件数'
    print '9:统计本月快递总数'
    print '10:统计每人昨天发件数'
    print '11:上个月各人发件数'
    print '12:上个月各快递公司发件数'
    print '13：更新全部物流信息'

    #for x in lastMonth_everyone_everyday_count('LiuYun'):
    #    print x.NAME
    #for x,y in lastMonth_everyone_everyday_count('LiuYun').items():
    #    print x,y
    #print session.query(Last_Month_Record).filter(Last_Month_Record.NAME == 'LiuYun', Last_Month_Record.DATE == '2017-02-06').count()

    #query = session.query(Last_Month_Record).filter(Last_Month_Record.DANHAO.like('% %')).all()
    #for x in query:
    #    session.query(Last_Month_Record).filter(Last_Month_Record.DANHAO == x.DANHAO).update({Last_Month_Record.DANHAO: x.DANHAO.strip()})
    #    print x.DANHAO,"已去除空格"
    #session.commit()

    num = raw_input('请输入:')
    if num == '1':
        add_one_record('ed','3322968747930','2017-02-14')
    elif num == '2':
        find_one_record()
    elif num == '3':
        update_one_record()
    elif num == '4':
        getKD()
    elif num == '5':
        delete_one_record()
    elif num == '6':
        everyone_today_count()
    elif num == '7':
        everyone_month_count()
    elif num == '8':
        wuliu_month_count()
    elif num == '9':
        print all_wuliu_count()
    elif num == '10':
        everyone_yesterday_count()
    elif num == '11':
        everyone_last_month_count()
    elif num == '12':
        wuliu_last_month_count()
    elif num == '13':
        update_all_wuliu()