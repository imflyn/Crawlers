# coding=utf-8

import urllib, urllib2, cookielib, os
from bs4 import BeautifulSoup

from common import HttpHeaders

currentPath = os.getcwd()
print currentPath
try:
    os.mkdir("/qsbk")
except Exception:
    pass


def decoder(content):
    soup = BeautifulSoup(content)
    for tag in soup.find_all('div', class_='article block untagged mb15'):
        try:
            sub = tag.find('img')
            imgurl = sub.attrs['src']
            print(imgurl)
            request = urllib2.urlopen(imgurl)
            data = request.read()
            request.close
            file = open(currentPath + "\qsbk\\" + imgurl.split('/')[-1], 'wb')
            file.write(data)
            file.close()
        except AttributeError as e:
            print e


def page_loop(page=1):
    print "第%s页" % page
    url = "http://www.qiushibaike.com/imgrank/page/%s?s=4743721" % page
    request = urllib2.Request(url)
    print request.get_full_url()
    for key in HttpHeaders.headers:
        request.add_header(key, HttpHeaders.headers[key])
    request.add_header('Referer', 'http://www.qiushibaike.com/')
    request.add_header('Origin', 'http://www.qiushibaike.com/')
    request.add_header('Cookie',
                       'bdshare_firstime=1421821228300; _qqq_uuid_=6ad5a178f7450619dc6f2a91af4cd3a7ed765f4f; __utmt=1; _qqq_user_id=8655363; Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1421821228,1423038765,1423041805; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1423041950; __utma=210674965.2057819279.1421821228.1423038765.1423041805.3; __utmb=210674965.6.10.1423041805; __utmc=210674965; __utmz=210674965.1421821228.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)')
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        print e.reason, e.code, e.msg
        print '异常，程序已终止'
        return

    text = response.read()
    decoder(text)

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

