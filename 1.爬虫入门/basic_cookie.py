#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
为什么要使用Cookie呢？
Cookie，指某些网站为了辨别用户身份、进行session跟踪而储存在用户本地终端上的数据（通常经过加密）
CookieJar  —-派生—->  FileCookieJar  —-派生—–>  MozillaCookieJar 和 LWPCookieJar
"""

import urllib2
import cookielib

url = 'http://www.baidu.com'

# 1.获取Cookie保存到变量
cookie = cookielib.CookieJar()  # 声明一个CookieJar对象实例来保存cookie
handler = urllib2.HTTPCookieProcessor(cookie)  # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
opener = urllib2.build_opener(handler)  # 通过handler来构建opener
response = opener.open(url)  # 此处的open方法同urllib2的urlopen方法，也可以传入request
for item in cookie:
    print item
    print 'Name = '+item.name
    print 'Value = '+item.value


# 2.保存Cookie到文件
filename = 'E:/Test/cookie.txt'  # 设置保存cookie文件的路径
cookie = cookielib.MozillaCookieJar(filename)  # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
handler = urllib2.HTTPCookieProcessor(cookie)  # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
opener = urllib2.build_opener(handler)  # 通过handler来构建opener
response = opener.open(url)  # 创建一个请求，原理同urllib2的urlopen

# ignore_discard: save even cookies set to be discarded.
# ignore_expires: save even cookies that have expired. The file is overwritten if it already exists
# ignore_discard的意思是即使cookies将被丢弃也将它保存下来，ignore_expires的意思是如果在该文件中cookies已经存在，则覆盖原文件写入
cookie.save(ignore_discard=True, ignore_expires=True)  # 保存cookie文件


# 3.从文件获取Cookie并访问
filename = 'E:/Test/cookie.txt'  # 已保存cookie的文件位置
cookie = cookielib.MozillaCookieJar()  # 创建MozillaCookieJar实例对象
cookie.load(filename, ignore_discard=True, ignore_expires=True)  # 从文件中读取cookie内容到变量
handler = urllib2.HTTPCookieProcessor(cookie)  # 使用urllib2的HTTPCookieProcessor对象来创建cookie处理器
opener = urllib2.build_opener(handler)  # 通过handler创建一个handler
response = opener.open(url)  # 请求
print response.read()
