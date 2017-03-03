# -*- coding: utf-8 -*-

import os,shutil
from werkzeug.utils  import secure_filename
import csv,time
from MyPackage import main

UPLOAD_FOLDER='upload'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))
ALLOWED_EXTENSIONS = set(['csv'])
file_dir = os.path.join(basedir, UPLOAD_FOLDER)   # 文件路径

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

# 创建文件夹
def creat_file_dir():
    if not os.path.exists(file_dir):  # 如果文件夹不存在，则创建文件夹
        os.makedirs(file_dir)

# 检查文件名是否合法
def filename_check(f = None):
    if f and allowed_file(f):  # 判断是否是允许上传的文件类型
        fname=secure_filename(f)
        print fname
        return fname
    else:
        return False

# 检查是否存在重复文件名
def check_existed_filename(f = None):
    ii = 0
    for parent, dirnames, filenames in os.walk(file_dir):  # 遍历目录并调用数据库写入函数
        for filename in filenames:
            if filename == f:
                ii = ii + 1
    if ii == 0:
        return False
    else:
        return True

#  保存文件
def save_file(f,secure_filename):
    f.save(os.path.join(file_dir, secure_filename))  # 保存文件到upload目录

# 删除文件
def del_file(f = None):
    os.remove(os.path.join(file_dir, f))

# 打开csv文件,并对比数据库
def open_csv_to_save(f =None):
    with open(os.path.join(file_dir, f)) as csvFile:
        dictreader = csv.DictReader(csvFile)
    countcsv = 0
    for line in dictreader:
        if main.find_one_record(line['\xcc\xf5\xc2\xeb'])>0:
            countcsv = countcsv +1
    if countcsv >= 3:
        return True
    else:
        return False



# 移动文件
def mov_file(f = None):
    currentday_file_dir = os.path.join(file_dir, time.strftime("%Y-%m-%d", time.localtime()))
    if not os.path.exists(currentday_file_dir):  # 如果文件夹不存在，则创建文件夹
        os.makedirs(currentday_file_dir)
    shutil.move(os.path.join(file_dir, f), currentday_file_dir)