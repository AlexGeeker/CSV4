# -*- coding: utf-8 -*-

import re,urllib2
from subprocess import Popen, PIPE

print "本机的私网IP地址为：" + re.search('\d+\.\d+\.\d+\.\d+',Popen('ipconfig', stdout=PIPE).stdout.read()).group(0)
print "本机的公网IP地址为：" + re.search('\d+\.\d+\.\d+\.\d+',urllib2.urlopen("http://1212.ip138.com/ic.asp").read()).group(0)