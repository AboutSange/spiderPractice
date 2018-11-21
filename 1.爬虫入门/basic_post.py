#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib
import urllib2

values = {"username":"xxx","password":"xxx"}
data = urllib.urlencode(values)

url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
request = urllib2.Request(url,data)
response = urllib2.urlopen(request)
print response.read()
