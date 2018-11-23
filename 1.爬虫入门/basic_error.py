#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
HTTPError是URLError的子类。

HTTPError实例产生后会有一个code属性，这就是是服务器发送的相关错误号。
因为urllib2可以为你处理重定向，也就是3开头的代号可以被处理，并且100-299范围的号码指示成功，所以你只能看到400-599的错误号码。
"""

import urllib
import urllib2

url = r'http://www.zhihu.com'

values = {"xxx": "xxx"}
data = urllib.urlencode(values)

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
referer = r'http://www.zhihu.com/articles'
headers = {'User-Agent': user_agent, 'Referer': referer}

req = urllib2.Request(url, data, headers)

# 1.
# try:
#     urllib2.urlopen(req)
# except urllib2.HTTPError, e:
#     print e.code
# except urllib2.URLError, e:
#     print e.reason
# else:
#     print "OK"


# 2.
try:
    resp = urllib2.urlopen(req)
except urllib2.URLError, e:
    if hasattr(e, "code"):
        print 'code: {}'.format(e.code)
    if hasattr(e, "reason"):
        print 'reason: {}'.format(e.reason)
else:
    print "OK"
    print(resp.msg)
    print(resp.read())

print 'done'