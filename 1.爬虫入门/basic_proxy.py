#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
站点可能检测某段时间某个IP的访问次数
"""

import urllib2

enable_proxy = True

proxy_handler = urllib2.ProxyHandler({'http': 'http://some-proxy.com:8080'})  # type: url
null_proxy_handler = urllib2.ProxyHandler({})

if enable_proxy:
    opener = urllib2.build_opener(proxy_handler)
else:
    opener = urllib2.build_opener(null_proxy_handler)

urllib2.install_opener(opener)
