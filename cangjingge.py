# coding=utf-8
import urllib.request, urllib.error, urllib.parse
import os, codecs, time
from bs4 import BeautifulSoup
from common import HttpHeaders

HOST = 'http://www.av9.cc'

start_time = time.time()

cwdpath = os.getcwd()
cwdpath = cwdpath + "\\" + "藏经阁"
print(cwdpath)

proxy = urllib.request.ProxyHandler({'http': '127.0.0.1:8087'})
opener = urllib.request.build_opener(proxy)
urllib.request.install_opener(opener)
content = urllib.request.urlopen("http://www.av9.cc/Home/Index").read()
soup = BeautifulSoup(content)
main = soup.find('div', class_='category')
unit = main.find_all('div', class_='unit')
for hrefs in unit:
    href = hrefs.find('a')
    nextUrl = HOST + href.attrs['href']
    print(nextUrl)
    proxy = urllib.request.ProxyHandler({'http': '127.0.0.1:8087'})
    opener = urllib.request.build_opener(proxy)
    urllib.request.install_opener(opener)
    content = urllib.request.urlopen(nextUrl).read()
    next_soup = BeautifulSoup(content)
    # 标题
    title = next_soup.find('title').getText()
    print(title)
    # 番号
    data = next_soup.find('div', class_="left")
    fanhao = data.find('div', class_='data').getText()
    fanhao = fanhao.replace('\n', '')
    print(fanhao)
    # 封面
    content_right = next_soup.find('div', class_='content_right')
    juzhao_url = content_right.find('a', class_="fancybox").attrs['href']
    print(juzhao_url)
    dir = cwdpath + "\\" + fanhao
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("创建文件夹:" + dir)
    else:
        continue
    try:
        request = urllib.request.Request(juzhao_url)
        for key in HttpHeaders.headers:
            request.add_header(key, HttpHeaders.headers[key])
        response = urllib.request.urlopen(request)
        data = response.read()
    except urllib.error.HTTPError as e:
        print(e)
    title = title.replace(' ', '')
    filePath = dir + "\\" + title + ".jpg"
    print(filePath)
    if not os.path.exists(filePath):
        file = open(filePath, 'wb')
        file.write(data)
        file.close()
    # 剧照
    next_unit = next_soup.find('div', attrs={'id': 'gallery'})
    next_hrefs = next_unit.find_all('img')
    for next_href in next_hrefs:
        next_img_url = next_href.attrs['src']
        print(next_img_url)
        try:
            request = urllib.request.Request(next_img_url)
            for key in HttpHeaders.headers:
                request.add_header(key, HttpHeaders.headers[key])
            response = urllib.request.urlopen(request)
            data = response.read()
        except urllib.error.HTTPError as e:
            print(e)
        filePath = dir + "\\" + next_img_url.split('/')[-1]
        print(filePath)
        if not os.path.exists(filePath):
            file = open(filePath, 'wb')
            file.write(data)
            file.close()
    # 去下载
    download_url = "http://www.torrentkitty.org/search/%s" % fanhao
    print(download_url)
    try:
        opener = urllib.request.build_opener()
        urllib.request.install_opener(opener)
        request = urllib.request.Request(download_url)
        for key in HttpHeaders.headers:
            request.add_header(key, HttpHeaders.headers[key])
        response = urllib.request.urlopen(request)
        data = response.read()
    except urllib.error.HTTPError as e:
        print(e)
        continue
    download_soup = BeautifulSoup(data)
    main = download_soup.find('table', attrs={'id': 'archiveResult'})
    list = main.find_all('a')
    num = 0
    for tag in list:
        href = tag.attrs['href']
        if href.startswith('magnet:'):
            print(href)
            filePath = dir + "\\" + "链接" + ".txt"
            print(filePath)
            file = codecs.open(filePath, 'a', encoding='utf-8')
            num = num + 1
            index = str(num) + '.'
            try:
                file.write(index)
                file.write(href)
                file.write("\n")
                file.close()
            except Exception:
                continue

print('耗时:' + str((time.time() - start_time)))
print('结束')

