#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
模拟访问API接口

思路：
    0.确定请求方式：post还是get
    1.urllib2.urlopen：只接收url, data, timeout，不接受headers
    2.headers：urllib2.Request
    3.cookie

"""

import json
import urllib
import urllib2
import cookielib

login_url = r'https://task.renderbus.com/api/rendering/user/userLogin'
dest_url = r'https://task.renderbus.com/api/rendering/user/queryUser'

# cookie
cookie_path = r'E:/Test/cookie.txt'  # 保存cookie文件路径
cookie = cookielib.MozillaCookieJar(cookie_path)  # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie_handler = urllib2.HTTPCookieProcessor(cookie)  # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
opener = urllib2.build_opener(cookie_handler)  # 通过handler来构建opener


# 1.login_url
# data
values = {
    'fingerprint': 'xxx',
    'password': 'xxx',
    'rememberPassword': False,
    'userName': 'xxx'
}
data = json.dumps(values, ensure_ascii=False)  # 这里不用urlencode也可以

# headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
    'Referer': 'https://task.renderbus.com/login',
    'channel': '2',
    'DNT': '1',
    'Host': 'task.renderbus.com',
    'Origin': 'https://task.renderbus.com',
    'signature': 'rayvision2017',
    'userKey': '',
    'version': '1.0.0',
    'Content-Type': 'application/json'
}

request = urllib2.Request(login_url, data, headers)
response = opener.open(request)

# save cookie
cookie.save(ignore_discard=True, ignore_expires=True)

result = response.read()
print result

# user_key
result_dict = json.loads(result)
user_key = result_dict.get('data', {}).get('userKey')

# 2.dest_url
# 如果不传data，则为None，则默认为Get请求
data2 = {}
headers2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36',
    'Referer': 'https://task.renderbus.com/login',
    'channel': '2',
    'DNT': '1',
    'Host': 'task.renderbus.com',
    'Origin': 'https://task.renderbus.com',
    'signature': 'rayvision2017',
    'userKey': user_key,
    'version': '1.0.0',
    'platform': '2'
}
request2 = urllib2.Request(dest_url, data2, headers2)
response2 = opener.open(request2)
print response2.read()
