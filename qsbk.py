# coding=utf-8

import urllib, urllib2, cookielib, os
from bs4 import BeautifulSoup

from common import HttpHeaders

HOST = 'http://www.qiushibaike.com'
DIRNAME = 'qb'

currentPath = os.getcwd()
print currentPath
try:
    os.makedirs(currentPath + "\\" + DIRNAME)
except Exception as e:
    print e.message


def decode_page(content):
    soup = BeautifulSoup(content)
    for tag in soup.find_all('div', class_='thumb'):
        sub = tag.find('a')
        href = sub.attrs['href']
        request = urllib2.Request(HOST + href)
        print request.get_full_url()
        for key in HttpHeaders.headers:
            request.add_header(key, HttpHeaders.headers[key])
        request.add_header('Referer', 'http://www.qiushibaike.com/')
        request.add_header('Origin', 'http://www.qiushibaike.com/')
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError as e:
            print e.reason, e.code, e.msg
            print '异常，程序已终止'
            return
        data = response.read()
        if data is not None:
            decode_detail(data)


def decode_detail(content):
    soup = BeautifulSoup(content)
    for tag in soup.find_all('div', 'thumb'):
        try:
            sub = tag.find('img')
            href = sub.attrs['src']
            filename = sub.attrs['alt']
            print filename
            print "img url:" + href
            download_file(href, filename)
        except AttributeError as e:
            print e


def download_file(url, filename):
    request = urllib2.urlopen(url)
    data = request.read()
    filepath = currentPath + "\\" + DIRNAME + "\\" + filename + ".jpg"
    if not os.path.exists(filepath):
        file = open(filepath, 'wb')
        file.write(data)
        file.close()
    else:
        print('file exists!')


def page_loop(page=1):
    print "第%s页" % page
    url = "http://www.qiushibaike.com/imgrank/page/%s?s=4743947" % page
    request = urllib2.Request(url)
    print request.get_full_url()
    for key in HttpHeaders.headers:
        request.add_header(key, HttpHeaders.headers[key])
    request.add_header('Referer', 'http://www.qiushibaike.com/')
    request.add_header('Origin', 'http://www.qiushibaike.com/')
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        print e.reason, e.code, e.msg
        print '异常，程序已终止'
        return

    text = response.read()
    decode_page(text)
    page_loop(page + 1)


def login():
    url = 'http://www.qiushibaike.com/session.js'
    postData = {
        'login': '江东子弟何惧于天下',
        'password': '223512',
        'remember_me': 'checked',
        'duration': '-1'
    }
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    postData = urllib.urlencode(postData)
    headers = HttpHeaders.headers
    headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers['Referer'] = 'http://www.qiushibaike.com/'
    headers['Origin'] = 'http://www.qiushibaike.com'
    headers['Host'] = 'www.qiushibaike.com'
    request = urllib2.Request(url, postData, headers)
    print request.get_full_url()
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        print e.reason, e.code, e.msg
        print '异常，程序已终止'
        return

    text = response.read()
    text = unicode(text, 'utf-8').encode('gb2312')
    print text


login()
page_loop()

