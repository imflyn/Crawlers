# coding=utf-8
import urllib2


def login():
    url = 'http://www.baidu.com'
    request = urllib2.Request(url)
    try:
        response = urllib2.urlopen(request)
    except Exception as e:
        print(e)
        print '异常，程序已终止'
        return

    text = response.read()
    print text


login()

