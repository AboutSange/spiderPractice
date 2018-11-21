#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib2
request = urllib2.Request('<URL:http://www.baidu.com>')
print(request)
response = urllib2.urlopen(request)
print type(response)

# import re
# _queryprog = re.compile('^(.*)#([^#]*)$')
# m = _queryprog.match(r'http://www.baidu.com/aa#11.jpg#fds')
# print m.group(1, 2)

