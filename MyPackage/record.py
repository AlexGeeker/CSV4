# -*- coding: utf-8 -*-

from sqlalchemy import Column, TEXT, create_engine,Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import time,datetime

tableName = 'KDTJ'+time.strftime("%Y%m", time.localtime())
# 上个月的tablename
today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lastMonthTable = 'KDTJ'+lastMonth.strftime("%Y%m")

Base = declarative_base()
class Record(Base):
    __tablename__ = tableName
    ID = Column(Integer, primary_key=True, autoincrement=True)
    NAME = Column(TEXT, nullable=False)
    DANHAO = Column(TEXT, nullable=False)
    WULIU = Column(TEXT, nullable=False)
    DATE = Column(TEXT)

    def __init__(self,name,danhao,wuliu,date):
        self.NAME = name
        self.DANHAO = danhao
        self.WULIU = wuliu
        self.DATE = date

class Last_Month_Record(Base):
    __tablename__ = lastMonthTable
    ID = Column(Integer, primary_key=True, autoincrement=True)
    NAME = Column(TEXT, nullable=False)
    DANHAO = Column(TEXT, nullable=False)
    WULIU = Column(TEXT, nullable=False)
    DATE = Column(TEXT)

    def __init__(self,name,danhao,wuliu,date):
        self.NAME = name
        self.DANHAO = danhao
        self.WULIU = wuliu
        self.DATE = date

class Products2(Base):
    __tablename__ = 'products2'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(TEXT, nullable=False)
    url_ID = Column(TEXT)
    img = Column(TEXT)
    code = Column(TEXT,unique=True)
    subProducts = relationship('subProducts',backref="products2")

    def __init__(self, name, url_ID, img, code, subProducts = []):
        self.name = name
        self.url_ID = url_ID
        self.img = img
        self.code = code
        self.subProducts = subProducts

class subProducts(Base):
    __tablename__ = 'subproducts'
    ID = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(TEXT, nullable=False)
    code = Column(TEXT,unique=True)
    Products_id = Column(Integer, ForeignKey('products2.ID'))

    def __init__(self, name, code):
        self.name = name
        self.code = code
