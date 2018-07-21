import requests
import os
import time
import random
from lxml import etree


def get_page_source(url, headers):
    print('get_page_source.......')
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('获取页面失败！！！')

def parse_page_source(html):
    print('parse_page_source...')
    hrefs = []
    html = etree.HTML(html)
    hrefs1 = html.xpath('//div[@class="col-sm-9"]/a[contains(@class,"list-group-item")]/@href')
    for href in hrefs1:
        print('系列链接:  ' + href)
        hrefs.append(href)

    return hrefs


def get_img(href, headers):
    print('get_img...')
    try:
        r = requests.get(href, headers=headers)
        r.raise_for_status
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('获取图片页面失败！！！')

def parse_img(img_html):
    print('parse_img...')
    srcs = []
    html = etree.HTML(img_html)
    srcs1 = html.xpath('//div[@class="pic-content"]//td//img/@src')
    for src in srcs1:
        print('图片地址：  ' + src)
        srcs.append(src)
    return srcs

def sava_img(src, headers):
    print('save_img...')
    
    file_name = src.split('/')[-1]
    if not os.path.exists(file_name):
        if src:
            r = requests.get(src, headers=headers)
            with open(file_name, 'wb') as f:
                f.write(r.content)
                print('保存成功')
        else:
            print('未获得图片地址')
    else:
        print('文件已存在')

def main(i):
    base_url = 'https://www.doutula.com/article/list/?page='
    page = i
    url = base_url + str(page)
    headers = {
        'User-Agent':str(ua())
        }
    html = get_page_source(url, headers)
    hrefs = parse_page_source(html)
    for href in hrefs:
        img_html = get_img(href, headers)
        srcs = parse_img(img_html)
        for src in srcs:
            sava_img(src, headers=headers)

def ua():
    ua = ['Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
          'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0',
          'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
          ]
    return random.choice(ua)
if __name__ == '__main__':
    for i in range(100000):
        print('获取第' + str(i) + '页的斗图')
        main(i)
        time.sleep(5)
    
