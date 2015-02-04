# coding =utf8

from bs4 import BeautifulSoup
import urllib2, os, sys
import HttpHeaders


def page_loop(page=1):
    url = "http://www.qiushibaike.com/8hr/page/%s?s=4743462" % page
    request = urllib2.Request(url)
    for key in HttpHeaders.headers:
        request.add_header(key, HttpHeaders.headers[key])
    response = urllib2.urlopen(request)





