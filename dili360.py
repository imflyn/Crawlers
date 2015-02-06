import urllib.request, urllib.error, urllib.parse
import os
from bs4 import BeautifulSoup
from common import HttpHeaders

HOST = 'http://www.dili360.com'

cwdpath = os.getcwd()
cwdpath = cwdpath + "\\" + "中国国家地理"
print(cwdpath)


def getGalleryList(content):
    soup = BeautifulSoup(content)
    left_side = soup.find('ul', class_='gallery-cate-list')
    active = left_side.find_all('li')
    gallery = {}
    for tag in active:
        hrefs = tag.find_all('a')
        for href in hrefs:
            url = href.attrs['href']
            if len(url) < 10:
                continue
            column = href.getText()
            gallery[column] = HOST + url
    print(gallery)
    return gallery


def parse_img_list(content, column):
    soup = BeautifulSoup(content)
    main = soup.find('ul', class_='gallery-block-small')
    gallery = main.find_all('div', class_='img')
    if len(gallery) == 0:
        return False
    for detail in gallery:
        href = detail.find('a')
        detail_url = HOST + href.attrs['href']
        title = href.attrs['title']
        # 创建文件夹
        title = title.strip().replace(' ', '').replace('\t', '')
        dir = cwdpath + "\\" + column + "\\" + title
        print(detail_url, title)
        if not os.path.exists(dir):
            os.makedirs(dir)
            print("创建文件夹:" + dir)
        parse_detail(detail_url, dir)
    return True


def parse_detail(url, dir):
    try:
        content = urllib.request.urlopen(url).read()
    except urllib.error.HTTPError as e:
        print(e)
    soup = BeautifulSoup(content)
    main = soup.find('ul', class_='slider')
    source_list = main.find_all('li')
    index = 0
    for tag in source_list:
        url = tag.attrs['data-source']
        title = tag.attrs['data-text']
        print("图片网址:" + url)
        print(title)
        index = index + 1
        save_img(url, dir, str(index))
        save_info(title, dir, str(index))


def save_info(title, filedir, index):
    filePath = filedir + "\\" + "文字说明" + ".txt"
    print(filePath)
    file = open(filePath, 'a')
    index = index + '.'
    file.write(index)
    file.write(title)
    file.write("\n")
    file.close()


def save_img(url, filedir, filename):
    try:
        request = urllib.request.Request(url)
        for key in HttpHeaders.headers:
            request.add_header(key, HttpHeaders.headers[key])
        response = urllib.request.urlopen(request)
        data = response.read()
    except urllib.error.HTTPError as e:
        print(e)
        return
    try:
        if not os.path.exists(filedir):
            os.makedirs(filedir)
    except Exception as e:
        print(e)
    filePath = filedir + "\\" + filename + ".jpg"
    print(filePath)
    if not os.path.exists(filePath):
        file = open(filePath, 'wb')
        file.write(data)
        file.close()
        print('保存成功')
    else:
        print('文件已存在')


def getContent(url):
    str = urllib.request.urlopen(url).read()
    return str


def page_loop(url, page=1):
    url2 = url % page
    print(url2)
    # 获取网页内容
    try:
        response = urllib.request.urlopen(url2);
        html = response.read()
    except AttributeError as e:
        print(e.reason)
        return
    if parse_img_list(html, column):
        page_loop(url, int(page) + 1)


# ========================过程========================

content = getContent('http://www.dili360.com/gallery')
gallery = getGalleryList(content)

for (column, url) in gallery.items():
    # 先创建文件夹:
    dir = cwdpath + "\\" + column
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("创建文件夹:" + dir)
    url = url.replace(".htm", "/%s.htm")
    page_loop(url, 1)







