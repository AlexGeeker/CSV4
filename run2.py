# -*- coding: utf-8 -*-

from flask import Flask,render_template,redirect,url_for,flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from MyPackage import main,products
import os,csv,time,shutil,random
from werkzeug.utils  import secure_filename
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields import SelectField,RadioField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from datetime import date,timedelta
from MyPackage.products import Product,subProduct
from MyPackage.record import Products2,subProducts,Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,relationship

engine = create_engine("sqlite:///C:\Users\Administrator\PycharmProjects\CSV\KDTJ.db", echo=False)
Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

currentdate = time.strftime("%Y-%m-%d", time.localtime())

today = date.today()
yesterday = date.today() - timedelta(1)
twoday = date.today() - timedelta(2)
threeday = date.today() - timedelta(3)
fourday = date.today() - timedelta(4)

app = Flask(__name__)
manager = Manager(app)
app.config['SECRET_KEY'] = 'hard to guess string110120'
bootstrap = Bootstrap(app)
moment = Moment(app)

UPLOAD_FOLDER='upload'
PRODUCT_IMG_FOLDER = 'static/product_img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['csv'])
file_dir = os.path.join(basedir, UPLOAD_FOLDER)   # 文件路径

# 查询单号表单
class DanhaoForm(FlaskForm):
    danhao = StringField(u'单号查询，请输入单号：', validators=[Required()])
    submit = SubmitField(u'提交')

# 上传文件表单
class UploadForm(FlaskForm):
    file = FileField( u'选择CSV文件:',validators=[
        FileAllowed(['csv'], u'只能上传csv文件！'),
        FileRequired(u'文件未选择！')])
    date = SelectField(u'选择发货日期:', choices=[
        (str(today), today),
        (str(yesterday), yesterday),
        (str(twoday), twoday),
        (str(threeday), threeday),
        (str(fourday), fourday)])
    name = RadioField(u'选择姓名:', choices=[
        ('WeiSui', u'韦随'),
        ('HuangShuo', u'黄硕'),
        ('LiJinSheng', u'李金生'),
        ('LiuYun', u'刘云')],
        validators=[DataRequired()])
    submit = SubmitField(u'上传')

# 上传产品表单
class UploadProduct(FlaskForm):
    # 上传图片
    imgfile = FileField( u'选择图片:',validators=[
        FileAllowed(['jpg','png','jpeg'], u'只能上传jpg,png,jpeg！'),
        FileRequired(u'文件未选择！')])
    # 产品名称
    product_name = StringField(u'产品名称：', validators=[Required()])
    # 产品ID
    product_ID = StringField(u'产品ID：', validators=[Required()])
    # 产品编码
    product_code = StringField(u'产品编码：', validators=[Required()])
    # 上传按钮
    submit = SubmitField(u'上传')

# 编辑产品及子产品表单
class EditProduct(FlaskForm):
    product_name = StringField(u'产品名称：', validators=[Required()])
    product_ID = StringField(u'产品ID：', validators=[Required()])
    product_code = StringField(u'产品编码：', validators=[Required()])
    # 子产品
    subproduct_name = StringField(u'颜色分类：', validators=[Required()])
    subproduct_code = StringField(u'颜色分类编码：', validators=[Required()])

    submit = SubmitField(u'更新')
# 添加子产品表单
class addSubproduct(FlaskForm):
    subproduct_name = StringField(u'颜色分类名称：', validators=[Required()])
    subproduct_code = StringField(u'产品编码：', validators=[Required()])
    submit = SubmitField(u'添加')

@app.route('/', methods=['GET', 'POST'])
def index():
    # 从网页获取单号
    danhao = None
    form = DanhaoForm()
    if form.validate_on_submit():
        danhao = form.danhao.data
        danhao = danhao.strip()  # strip()的作用是去掉左右空格
        form.danhao.data = ''

    # 查询单号（本月及上月）
    allDanhao = main.find_one_record(danhao)

    # 本月快递总数
    allCount = main.all_wuliu_count()
    # 本月各快递总数
    kuaidicount = main.wuliu_month_count()
    # 本月所有人发件数
    everyoneCount = main.everyone_month_count()
    # 昨天各人发件数
    yesterdayCount = main.everyone_yesterday_count()
    # 今天各人发件数
    todayCount = main.everyone_today_count()
    # 上个月各快递公司总数
    lastMonth_kuaidicount = main.wuliu_last_month_count()
    # 每人上个月发件数
    lastMonth_everyoneCount = main.everyone_last_month_count()

    return render_template('index.html', form=form, check_record=allDanhao,total=allCount,kuaiditotal = kuaidicount,everyoneCount=everyoneCount,yesterdayCount = yesterdayCount,todayCount = todayCount,lastMonth_kuaidicount = lastMonth_kuaidicount,lastMonth_everyoneCount = lastMonth_everyoneCount)

# 下面是上传文件部分

# 用于判断文件后缀
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/api/upload',methods=['GET', 'POST'],strict_slashes=False)
def api_upload():
    form = UploadForm()
    fname = None
    name = None
    selected_date = None
    existed_record = 0
    recorded = 0
    if form.validate_on_submit():

        selected_date = form.date.data
        name = form.name.data
        #f = request.files['file']
        #fname = secure_filename(f.filename)
        fname = secure_filename(form.file.data.filename)

        file_dir=os.path.join(basedir,app.config['UPLOAD_FOLDER']) # 文件路径
        if not os.path.exists(file_dir): # 如果文件夹不存在，则创建文件夹
            os.makedirs(file_dir)

        # 文件名重复判断
        ii = 0
        for parent, dirnames, filenames in os.walk(file_dir):  # 遍历目录并调用数据库写入函数
            for filename in filenames:
                if filename == fname:
                    ii = ii + 1
        if ii == 0:
            form.file.data.save(os.path.join(file_dir, fname))  # 保存文件到upload目录
        else:
            return render_template('upload2.html', form = form, filename=fname, message=u'该文件已存在，请重新上传！')

        # 读取文件，并对比数据库

        with open(os.path.join(file_dir, fname)) as csvFile:
            dictreader = csv.DictReader(csvFile)
            for line in dictreader:
                if main.find_one_record(line['\xcc\xf5\xc2\xeb']):  # 如果单号已经存在于数据中
                    existed_record = existed_record +1
                else:  # 若单号不在数据库中，则写入数据库
                    recorded = recorded + 1
                    main.add_one_record(name, line['\xcc\xf5\xc2\xeb'], selected_date)

        # 创建当天日期文件夹，并将文件转移至该文件夹
        currentday_file_dir = os.path.join(file_dir, selected_date)
        if not os.path.exists(currentday_file_dir):  # 如果文件夹不存在，则创建文件夹
            os.makedirs(currentday_file_dir)
        shutil.move(os.path.join(file_dir, fname), currentday_file_dir)

    return render_template('upload2.html', form=form, filename=fname, name=name, date=selected_date,recorded = recorded,existed_record = existed_record)

# 上传产品
@app.route('/upload/product',methods=['GET', 'POST'])
def upload_product():
    form = UploadProduct()
    imgName = None
    message = None

    if form.validate_on_submit():
        # 上传的图片名：时间+随机数
        ext = os.path.splitext(form.imgfile.data.filename)[1]
        imgName = time.strftime("%Y%m%d%H%M%S", time.localtime()) + '_%d' % random.randint(0,100) + ext
        # 产品名称
        product_name = form.product_name.data
        # 产品id
        product_id = form.product_ID.data
        # 产品编码
        product_code = form.product_code.data

        # 创建产品图片文件夹
        file_dir=os.path.join(basedir,PRODUCT_IMG_FOLDER) # 文件路径
        if not os.path.exists(file_dir): # 如果文件夹不存在，则创建文件夹
            os.makedirs(file_dir)
        # 保存图片至文件夹
        form.imgfile.data.save(os.path.join(file_dir, imgName))

        product_x = Product(product_name,product_id,imgName,product_code)
        product_x.add_one_product()
        message = u"上传成功"


    return render_template('upload_product.html',form = form,name = imgName,message = message)


# 删除一个产品
@app.route('/delete-product/<int:id>',methods=['GET', 'POST'])
def del_product(id):
    products.delete_product(id)
    return redirect(url_for('all_product'))

# 编辑产品
@app.route('/edit-product/<int:id>',methods=['GET', 'POST'])
def edit_product(id):
    form = EditProduct()
    # 产品
    product_to_edit = products.get_product_from_id(id)
    # 子产品
    #subproducts_to_edit = products.subproduct(id)
    subproducts_to_edit = product_to_edit.subProducts

    img = product_to_edit.img

    #imgurl = "/static/product_img/"+product_to_edit.img

    # 修改信息
    if form.validate_on_submit():
        name = form.product_name.data
        url_ID = form.product_ID.data
        code = form.product_code.data

        #Products2.query.get(1)

        subproduct_name = form.subproduct_name.data
        subproduct_code = form.subproduct_code.data
        # 若没有子产品，则添加一个子产品
        if subproducts_to_edit == []:
            new_subproduct = subProduct(subproduct_name,subproduct_code)
            new_subproduct.add_one_subproduct()
        else:
            # 更新子产品
            products.update_subproduct(id, subproduct_name,id)

        # 更新产品
        products.update_product(id,name,url_ID,img,code)


        #productx = Product(name,url_ID,img,code)
        #productx.add_one_product()
        #flash("编辑成功！")
        return redirect(url_for('all_product'))

    form.product_name.data = product_to_edit.name
    form.product_ID.data = product_to_edit.url_ID
    form.product_code.data = product_to_edit.code
    # 子产品
    if subproducts_to_edit == []:
        form.subproduct_name.data = None
        form.subproduct_code.data = None
    else:
        form.subproduct_name.data = subproducts_to_edit[0].name
        form.subproduct_code.data = subproducts_to_edit[0].code

    return render_template('edit_product.html',form = form,product_to_edit= product_to_edit)
    #return redirect(url_for('upload_product'))

# 全部产品
@app.route('/product', methods=['GET', 'POST'])
def all_product():
    subproducts = None
    allproducts = products.all_products()
    return render_template('products.html', allproducts=allproducts, subproducts=subproducts)

# 产品页
@app.route('/product/<int:id>', methods=['GET', 'POST'])
def id_product(id):
    # 子产品
    #subproducts = products.subproduct(id)
    # 全部产品
    allproducts = products.all_products()

    return render_template('products.html',allproducts = allproducts)

# 显示图片
@app.route('/upload/product_img/<imgname>', methods=['GET', 'POST'])
def img(imgname):
    imgname = "/upload/product_img/" + imgname
    return imgname

# 显示上个月每天每人发件数
@app.route('/<user_name>', methods=['GET', 'POST'])
def show_last_month_data(user_name):
    count = main.lastMonth_everyone_everyday_count(user_name)
    return render_template('lastmonth.html',count = count)

# 添加子产品
@app.route('/product/add_subproduct/<int:id>', methods=['GET', 'POST'])
def add_subproduct(id):
    product_to_edit = session.query(Products2).get(id)
    form = addSubproduct()
    if form.validate_on_submit():
        name = form.subproduct_name.data
        code = form.subproduct_code.data
        sub1= subProducts(name,code)
        product_to_edit.subProducts.append(sub1)
        session.add(product_to_edit)
        session.commit()
        return redirect(url_for('all_product'))

    return render_template('add_subproduct.html', product_to_edit=product_to_edit,form = form)
if __name__ == '__main__':
    app.run(debug=True)