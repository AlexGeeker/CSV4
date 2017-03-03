# -*- coding: utf-8 -*-

from flask import Flask,render_template,request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from MyPackage import main
import os,csv,time,shutil
from werkzeug.utils  import secure_filename
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields import SelectField
from flask_wtf import FlaskForm

currentdate = time.strftime("%Y-%m-%d", time.localtime())

app = Flask(__name__,static_folder='C:\Users\Administrator\PycharmProjects\CSV')
manager = Manager(app)
app.config['SECRET_KEY'] = 'hard to guess string110120'
bootstrap = Bootstrap(app)
moment = Moment(app)

UPLOAD_FOLDER='upload'
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
    file = FileField( u'选择CSV文件',validators=[
        FileAllowed(['csv'], u'只能上传csv文件！'),
        FileRequired(u'文件未选择！')])
    name = SelectField(u'姓名', choices=[
        ('WeiSui', u'韦随'),
        ('HuangShuo', u'黄硕'),
        ('LiJinSheng', u'李金生'),
        ('LiuYun', u'刘云')
    ])
    submit = SubmitField(u'上传')

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


# 用于测试上传，稍后用到
@app.route('/test/upload')
def upload_test():
#    form = UploadForm()
    return render_template('upload.html')

@app.route('/api/upload',methods=['GET', 'POST'],strict_slashes=False)
def api_upload():

    file_dir=os.path.join(basedir,app.config['UPLOAD_FOLDER']) # 文件路径
    if not os.path.exists(file_dir): # 如果文件夹不存在，则创建文件夹
        os.makedirs(file_dir)

    f=request.files['myfile']  # 从表单的file字段获取文件，myfile为该表单的name值

    # 文件名后缀判断
    if f and allowed_file(f.filename):  # 判断是否是允许上传的文件类型
        fname = secure_filename(f.filename)
        print fname
    else:
        return render_template('upload.html', message=u"文件名错误，上传失败！")

    # 文件名重复判断
    ii = 0
    for parent, dirnames, filenames in os.walk(file_dir):  # 遍历目录并调用数据库写入函数
        for filename in filenames:
            if filename == fname:
                ii = ii + 1
    if ii == 0:
        f.save(os.path.join(file_dir, fname))  # 保存文件到upload目录
    else:
        return render_template('upload.html', filename=fname, message=u'该文件已存在，请重新上传！')

    # 读取文件，并对比数据库
    with open(os.path.join(file_dir, fname)) as csvFile:
        dictreader = csv.DictReader(csvFile)
        existed_record = 0
        recorded = 0
        for line in dictreader:
            if main.find_one_record(line['\xcc\xf5\xc2\xeb']):  # 如果单号已经存在于数据中
                existed_record = existed_record +1
            else:  # 若单号不在数据库中，则写入数据库
                recorded = recorded + 1
                if 'HS' in fname:
                    main.add_one_record('HuangShuo', line['\xcc\xf5\xc2\xeb'], currentdate)
                elif 'LY' in fname:
                    main.add_one_record('LiuYun', line['\xcc\xf5\xc2\xeb'], currentdate)
                elif 'LJS' in fname:
                    main.add_one_record('LiJinSheng', line['\xcc\xf5\xc2\xeb'], currentdate)
                elif 'WS' in fname:
                    main.add_one_record('WeiSui', line['\xcc\xf5\xc2\xeb'], currentdate)

    # 创建当天日期文件夹，并将文件转移至该文件夹
    currentday_file_dir = os.path.join(file_dir, time.strftime("%Y-%m-%d", time.localtime()))
    if not os.path.exists(currentday_file_dir):  # 如果文件夹不存在，则创建文件夹
        os.makedirs(currentday_file_dir)
    shutil.move(os.path.join(file_dir, fname), currentday_file_dir)

    return render_template('upload.html',filename=fname, existed_record =existed_record,recorded =recorded)

@app.route('/update')
def update():
    updates = main.update_all_wuliu()
    return render_template('update.html',message = updates)

if __name__ == '__main__':
    app.run(debug=True)