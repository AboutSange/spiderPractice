#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
检测是否爬虫访问：检测请求头、反盗链（识别referer）
需注意的属性：
    User-Agent : 有些服务器或 Proxy 会通过该值来判断是否是浏览器发出的请求
    Content-Type : 在使用 REST 接口时，服务器会检查该值，用来确定 HTTP Body 中的内容该怎样解析。
    application/xml ： 在 XML RPC，如 RESTful/SOAP 调用时使用
    application/json ： 在 JSON RPC 调用时使用
    application/x-www-form-urlencoded ： 浏览器提交 Web 表单时使用
    在使用服务器提供的 RESTful 或 SOAP 服务时， Content-Type 设置错误会导致服务器拒绝服务
"""

import urllib
import urllib2

url = r'http://www.zhihu.com'

values = {'username': 'xxx', 'password': 'xxx'}
data = urllib.urlencode(values)

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
referer = r'http://www.zhihu.com/articles'
headers = {
    'User-Agent': user_agent,
    'Referer': referer
}

request = urllib2.Request(url, data, headers)

response = urllib2.urlopen(request)
print(response.headers)
print(response.url)
print(response.code)
print(response.msg)
print(response.info())
# print(response.read())


