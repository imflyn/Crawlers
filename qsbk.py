import urllib.request, urllib.error, urllib.parse, http.cookiejar
import os, time
from bs4 import BeautifulSoup
from common import HttpHeaders

HOST = 'http://www.qiushibaike.com'
DIRNAME = 'qb'

currentPath = os.getcwd() + "\\" + DIRNAME + "\\" + time.strftime('%Y%m%d', time.localtime(time.time()))
print(currentPath)
try:
    if not os.path.exists(currentPath):
        os.makedirs(currentPath)
except Exception as e:
    print(e)


def decode_page(content):
    soup = BeautifulSoup(content)
    for tag in soup.find_all('div', class_='thumb'):
        sub = tag.find('a')
        href = sub.attrs['href']
        request = urllib.request.Request(HOST + href)
        print(request.get_full_url())
        for key in HttpHeaders.headers:
            request.add_header(key, HttpHeaders.headers[key])
            request.add_header('Referer', 'http://www.qiushibaike.com/')
            request.add_header('Origin', 'http://www.qiushibaike.com/')
        try:
            response = urllib.request.urlopen(request)
        except urllib.error.HTTPError as e:
            print(e.reason, e.code, e.msg)
            print('异常，程序已终止')
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
            print(filename)
            print("img url:" + href)
            download_file(href, filename)
        except AttributeError as e:
            print(e)


def download_file(url, filename):
    request = urllib.request.urlopen(url)
    data = request.read()
    filepath = currentPath + "\\" + filename + ".jpg"
    if not os.path.exists(filepath):
        file = open(filepath, 'wb')
        file.write(data)
        file.close()
    else:
        print('file exists!')


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
        print('异常，程序已终止')
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
        print('异常，程序已终止')
        return

    text = response.read()
    print(text)


login()
page_loop()


