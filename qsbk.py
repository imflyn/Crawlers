import urllib.request, urllib.error, urllib.parse, http.cookiejar
import os
from bs4 import BeautifulSoup
from common import HttpHeaders

MASTER_NAME = '大神戴腾的爪牙'

HOST = 'http://www.qiushibaike.com'
DIRNAME = 'qb'

cwdpath = os.getcwd()
print(cwdpath)


def decode_page(content):
    soup = BeautifulSoup(content)
    for tag in soup.find_all('div', class_='thumb'):
        sub = tag.find('a')
        href = sub.attrs['href']
        request = urllib.request.Request(HOST + href)
        print(MASTER_NAME + "打开了网页: <" + request.get_full_url() + ">")
        for key in HttpHeaders.headers:
            request.add_header(key, HttpHeaders.headers[key])
        request.add_header('Referer', 'http://www.qiushibaike.com/')
        request.add_header('Origin', 'http://www.qiushibaike.com/')
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            print(e.reason, e.code, e.msg)
            print('出现异常，%s已停止运行' % MASTER_NAME)
            return
        data = response.read()
        if data is not None:
            decode_detail(data)


def decode_detail(content):
    soup = BeautifulSoup(content)
    for tag in soup.find_all('div', class_='content'):
        submit_date = tag.attrs['title']
        submit_date = submit_date.split(' ')[0]
    for tag in soup.find_all('div', class_='thumb'):
        try:
            sub = tag.find('img')
            href = sub.attrs['src']
            filename = sub.attrs['alt']
            print(MASTER_NAME + "发现标题: <" + filename + ">")
            print(MASTER_NAME + "发现链接: <" + href + ">")
            download_file(href, submit_date, filename)
        except AttributeError as e:
            print(e)
            print('出现异常，%s已停止运行' % MASTER_NAME)


def download_file(url, date, filename):
    request = urllib.request.urlopen(url)
    data = request.read()
    fileDir = cwdpath + "\\" + DIRNAME + "\\" + date
    try:
        if not os.path.exists(fileDir):
            os.makedirs(fileDir)
    except Exception as e:
        print(e)
        print('出现异常，%s已停止运行' % MASTER_NAME)
    filePath = fileDir + "\\" + filename + ".jpg"
    if not os.path.exists(filePath):
        file = open(filePath, 'wb')
        file.write(data)
        file.close()
        print(MASTER_NAME + "保存文件成功!")
    else:
        print(MASTER_NAME + "侦测到文件已存在,未下载!")


def page_loop(page=1):
    print("第%s页" % page)
    url = "http://www.qiushibaike.com/imgrank/page/%s?s=4743947" % page
    request = urllib.request.Request(url)
    print(request.get_full_url())
    for key in HttpHeaders.headers:
        request.add_header(key, HttpHeaders.headers[key])
    request.add_header('Referer', 'http://www.qiushibaike.com/')
    request.add_header('Origin', 'http://www.qiushibaike.com/')
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        print(e.reason, e.code, e.msg)
        print('出现异常，%s已停止运行' % MASTER_NAME)
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
    cj = http.cookiejar.LWPCookieJar()
    cookie_support = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    postDataStr = urllib.parse.urlencode(postData)
    headers = HttpHeaders.headers
    headers['Accept'] = 'application/json, text/javascript, */*; q=0.01'
    headers['Referer'] = 'http://www.qiushibaike.com/'
    headers['Origin'] = 'http://www.qiushibaike.com'
    headers['Host'] = 'www.qiushibaike.com'
    request = urllib.request.Request(url=url, data=postDataStr.encode("utf-8"), headers=headers, method='POST')
    print(request.get_full_url())
    try:
        response = urllib.request.urlopen(request)
    except urllib.error.HTTPError as e:
        print(e.reason, e.code, e.msg)
        print('出现异常，%s已停止运行' % MASTER_NAME)
        return

    text = response.read()
    print(text)
    print(MASTER_NAME + "登录了糗百网页")


login()
page_loop()


