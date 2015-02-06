# coding=utf-8
import urllib.request
import time, re


str = 'http://www.dili360.com/gallery/cate/2/1.htm'
rs = re.search('/', str)
print(rs.endpos - 1)

print(str(str.index(rs.endpos - 1)))