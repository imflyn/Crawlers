# coding=utf-8
import urllib.request
import time


def login():
    url = 'http://www.baidu.com'
    request = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(request)
    except Exception as e:
        print(e)
        print('异常，程序已终止')
        return

    text = response.read()
    print(text)


# login()
print(time.strftime('%Y%m%d', time.localtime(time.time())))
