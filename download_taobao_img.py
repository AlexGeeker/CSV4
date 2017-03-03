# -*- coding: utf-8 -*-

from urllib import urlopen
from urllib2 import HTTPError
from bs4 import BeautifulSoup
import re

#url = 'https://detail.tmall.com/item.htm?spm=a1z10.3-b.w4011-2630292284.138.oManFd&id=544533009503&rn=73a8455e91f6c021898a03c9b5b8bf26&abbucket=12'
#html = urlopen(url)

class URL:
    url = None
    def __init__(self,url):
        self.url = str(url)
        URL.url = "https://detail.tmall.com/item.htm?id=" + self.url

    # 获取第一张主图链接
    def get_first_img(self):
        first_images = re.findall(r"t\":\[\".+pic.jpg", urlopen(URL.url).read())
        first_image_url = re.findall(r"\/\/.+pic.jpg",first_images[0])
        print "https:"+first_image_url[0]
        return "https:"+first_image_url[0]

    # 获取全部四张主图
    def get_four_img(self):
        images = re.findall("t\":\[\".*jpg", urlopen(url).read())
        print images
        if images:
            print images[0]
            image_url = re.findall("\/\/.*jpg",images[0])
            print image_url[0]
            five_image = re.match(r'(\S+)","(\S+)","(\S+)","(\S+)","(\S+)', image_url[0])
            print five_image
            for i in range(1, 5):
                print "https:" + five_image.group(i)
        else:
            print '未匹配'
    # 获取标题
    def get_title(self):
        html = urlopen(URL.url)
        bs = BeautifulSoup(html,"html.parser")
        title = re.match('[^\-]+',bs.title.string)
        print title.group(0)

    # 获取完整url
    def get_full_url(self):
        print URL.url
        return URL.url

    # 获取颜色分类
    def get_color_fenlei(self):
        html = urlopen(URL.url)
        bs = BeautifulSoup(html,"html.parser")
        for i in bs.findAll("li"):
            print i.span

if __name__ == '__main__':
    print '1:下载第一张主图'
    print '2:下载4张主图'
    print '3:显示宝贝标题'
    print '4:显示完整链接'
    print '5:显示全部颜色分类'

    num = raw_input('请输入:')
    url = raw_input('请输入ID:')
    url = URL(url)

    if num == '1':
        url.get_first_img()
    if num == '2':
        url.get_four_img()
    if num == '3':
        url.get_title()
    if num == '4':
        url.get_full_url()
    if num == '5':
        url.get_color_fenlei()