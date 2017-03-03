# -*- coding: utf-8 -*-

from record import Products2,Base,subProducts
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy import create_engine
import time

engine = create_engine("sqlite:///C:\Users\Administrator\PycharmProjects\CSV\KDTJ.db", echo=False)
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

def mysession():
    return session()

class Product(object):
    def __init__(self, name, url_ID, img, code, subProducts = []):
        self.name = name
        self.url_ID = url_ID
        self.img = img
        self.code = code
        self.subProducts = subProducts

    # 添加一个产品
    def add_one_product(self):
        one_product = Products2(self.name, self.url_ID, self.img, self.code, self.subProducts)
        try:
            session.add(one_product)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    # 查找一个产品
    def show_all_products(self):
        return session.query(Products2).all()

class subProduct(object):

    def __init__(self, name, code):
        self.name = name
        self.code = code

    # 添加一个子产品
    def add_one_subproduct(self):
        new_subproduct = subProducts(self.name,self.code)
        session.add(new_subproduct)
        session.commit()
        session.close()

# 全部产品
def all_products():
    return session.query(Products2).all()

# 全部子产品
def all_subProducts():
    return session.query(subProducts).all()

# 产品的子产品
def subproduct(id):
    return session.query(Products2).get(id).subProducts

# 通过ID获取产品
def get_product_from_id(id):
    return session.query(Products2).get(id)

# 删除产品
def delete_product(id):
    product = session.query(Products2).get(id)
    session.delete(product)
    session.commit()
    session.close()
    print product.name + u"已删除"

# 编辑产品
def edit_product(id):
    Product = session.query(Products2).get(id)
    session.commit()
    session.close()

# 更新产品
def update_product(id,name,ID,img,code):
    #product_to_update = session.query(Products2).get(id)
    #session.query(product_to_update).update({"x": 5})
    #session.query.filter(Products2.id == id).update({User.name: 'c'})
    #session.query(Products2).get(id).update({Products2.name:name,Products2.url_ID:ID,Products2.img:img,Products2.code:code})
    session.query(Products2).filter(Products2.ID == id).update({Products2.name: name, Products2.url_ID: ID, Products2.img: img, Products2.code: code})
    session.commit()
    session.close()
    return True

# 更新子产品
def update_subproduct(id,name,ID):

    session.query(subProducts).filter(subProducts.ID == id).update({subProducts.name: name,subProducts.Products_id:ID})
    session.commit()
    session.close()
    return True

if __name__ == '__main__':
    #for x in all_products():
    #    print x.ID,x.name,x.code

    print session.query(Products2).get(10)
    '''
    print "1.添加一个产品"
    print "2.删除一个产品"
    print "3.添加一个子产品"

    print time.strftime("%Y%m%d%H%M%S", time.localtime())


    #product1 = Product('小夜灯1')
    #product1.subproduct1 = subProducts(u'白色白光','A-3-5')
    #print product1.getID()

    subproduct1 = subProducts(u'白色白光', 'A-3-9')
    #product1 = Products2(u'小夜灯1', '12345678', '/img/abc.jpg', 'A-8',subProducts = [subproduct1])
    product1 = Products2(u'小夜灯1', '12345678', '/img/abc.jpg', 'A-9')
    #product1.subProducts.append(subproduct1)

    num = raw_input('请输入:')

    if num == '1':
        session.add(product1)
        session.commit()
        session.close()
        #product1.add_one_product()
    if num == '2':
        #product1.delete_one_product()
        pass
    if num == '3':
       # subproduct1.add_one_subproduct()
        session.add(subproduct1)
        session.commit()
        session.close()
'''