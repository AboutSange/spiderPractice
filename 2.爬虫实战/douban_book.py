#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
根据标签爬取豆瓣图书（https://book.douban.com/tag）
1.单线程爬虫
2.多线程（池）爬虫
3.多进程（池）爬虫
4.异步IO爬虫
5.框架爬虫
"""



import os
import sys
import re
import time
import random
import urllib
import urllib2
from bs4 import BeautifulSoup
from openpyxl import Workbook

reload(sys)
sys.setdefaultencoding('utf-8')


def douban_book_spider(tag, debug=False):
    """
    根据tag收集待下载的url
    :param str tag: 标签
    :param bool debug: 如果为True，则打印详细信息
    :return:
    """
    page_num = 1  # 当前页数，从1开始
    try_times = 1  # 尝试次数
    book_list = []  # 书籍信息列表
    user_agent = r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
    headers = {'User-Agent': user_agent}

    while True:
        print 'Downloading page {0}'.format(page_num)
        # 随机sleep，5s以内
        time.sleep(random.random()*5)

        # 获取HTML
        url = u'https://www.douban.com/tag/{0}/book?start={1}'.format(urllib.quote(tag), str((page_num - 1) * 15))

        req = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(req)
        html = response.read()  # html/js

        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html, "lxml")  # <class 'bs4.BeautifulSoup'>
        soup2 = soup.find('div', {'class': 'mod book-list'})  # <class 'bs4.element.Tag'>

        # 如果为空页则重试3次，3次之后break循环
        if soup2 is None or len(soup2.contents) <= 1:
            try_times += 1
            if try_times > 3:
                break
            else:
                print '[Retry]',
                continue

        # 获取title, rating, dest信息
        for book_info in soup2.find_all('dd'):
            title = book_info.find('a', {'class': "title"}).string.strip()
            book_url = book_info.find('a', {'class': 'title'}).get('href')
            dest = book_info.find('div', {'class': "desc"}).string.strip()
            try:
                rating = book_info.find('span', {'class': "rating_nums"}).string.strip()
            except:
                rating = '0.0'

            if debug:
                print '{0}{1}'.format(' ' * 4, title)

            book_list.append([title, rating, dest])

        page_num += 1
    return book_list


def write_book_list_to_excel(book_list, book_tag):
    wb = Workbook()  # 默认生成一个名为'Sheet'的WorkSheet
    ws = sheet = wb.active
    sheet.title = book_tag.decode('utf-8')
    ws.append(['序号','书名','评分','出版信息'])
    count = 1
    for bl in book_list:
        ws.append([count, bl[0], float(bl[1]), bl[2]])
        count +=1

    save_path = u'book_list_{0}.xlsx'.format(book_tag.decode('utf-8'))
    wb.save(save_path)


def main():
    tag = "爬虫"
    book_list = douban_book_spider(tag=tag, debug=True)
    write_book_list_to_excel(book_list, tag)

if __name__ == '__main__':
    main()
