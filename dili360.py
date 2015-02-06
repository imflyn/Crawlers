import urllib.request, urllib.error, urllib.parse
import os
from bs4 import BeautifulSoup

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
    for detail in gallery:
        href = detail.find('a')
        imgUrl = HOST + href.attrs['href']
        title = href.attrs['title']
        # 创建文件夹
        title = title.strip().replace(' ', '').replace('\t', '')
        dir = cwdpath + "\\" + column + "\\" + title
        print(imgUrl, title)
        if not os.path.exists(dir):
            os.makedirs(dir)
            print("创建文件夹:" + dir)


def getContent(url):
    str = urllib.request.urlopen(url).read()
    return str

# ========================过程========================

content = getContent('http://www.dili360.com/gallery')
gallery = getGalleryList(content)

for (column, url) in gallery.items():
    # 先创建文件夹:
    dir = cwdpath + "\\" + column
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("创建文件夹:" + dir)

    # 获取网页内容
    html = urllib.request.urlopen(url).read()
    parse_img_list(html, column)







