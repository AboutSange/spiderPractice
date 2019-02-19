#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
爬取tripadvisor旅游网站
    title：标题
    img：图片地址
    rate：评分
    comment_num：评论数
"""

import requests
from bs4 import BeautifulSoup
import time

# 爬取纽约市景点活动信息
url_origin = r'https://www.tripadvisor.com.hk/Attractions-g60763-Activities-New_York_City_New_York.html'
urls = [r'https://www.tripadvisor.com.hk/Attractions-g60763-Activities-oa{0}-New_York_City_New_York.html'.format(str(i)) for i in range(30, 1260, 30)]
urls.insert(0, url_origin)

page_num = 1

for url in urls:
    time.sleep(2)
    print '\n'
    print '============{0}=============='.format(page_num)
    page_num += 1
    r = requests.get(url)  # r.text is the content of the response in unicode, and r.content is the content of the response in bytes.

    soup = BeautifulSoup(r.text, 'lxml')

    titles = soup.select('div.listing_title > a[target="_blank"]')  # [target="_blank"] 用来排除景点集合
    imgs = soup.select('img[width="180"]')
    rates = soup.select('div.listing_rating > div:nth-of-type(2) > div > span.ui_bubble_rating')
    comment_nums = soup.select('span.more > a')

    for title, img, rate, comment_num in zip(titles, imgs, rates, comment_nums):
        print u'title: {0}, '.format(title.get_text().strip()),
        print u'img: {0}, '.format(img.get('src')),
        print u'rate: {0}, '.format(rate.get('alt')),
        print u'comment_num: {0}'.format(comment_num.get_text().strip())
