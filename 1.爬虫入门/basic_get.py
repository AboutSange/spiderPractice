#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib
import urllib2

values={}
values['username'] = "xxx"
values['password']="xxx"
data = urllib.urlencode(values)

url = "http://passport.csdn.net/account/login"
geturl = url + "?"+data
request = urllib2.Request(geturl)
response = urllib2.urlopen(request)
print response.read()
