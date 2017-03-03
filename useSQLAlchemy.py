# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class jilu(Base):
    __tablename__ = 'CSV5'

    id = Column(Integer, primary_key=True)

engine = create_engine("sqlite:///C:/Users/Administrator/PycharmProjects/CSV/mycsv.db")
DBSession = sessionmaker(bind=engine)
session = DBSession()
#user = session.query(jilu).filter(jilu.DANHAO=='3322473008682').one()

print 'type:', type(engine)

session.commit()
session.close()