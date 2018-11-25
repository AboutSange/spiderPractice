#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import urllib2


class Spider(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
        }

    def get_html(self, url):
        """"获取URL的HTML并返回
        :param str url: URL
        :return: HTML or None(if error occurs)
        """
        request = urllib2.Request(url, headers=self.headers)
        try:
            response = urllib2.urlopen(request, timeout=6)
            result = response.read()
        except Exception as e:
            print e
            result = None
        return result


def main():
    patt = r'class="article block untagged mb15' \
           r'.*?' \
           r'class="author clearfix"' \
           r'.*?' \
           r'<h2>(.*?)</h2>' \
           r'.*?' \
           r'class="content".*?<span>(.*?)</span>' \
           r'.*?' \
           r'class="stats-vote"><i class="number">(.*?)</i>'
    print patt
    patt_new = re.compile(patt, re.S)

    sp = Spider()
    html = sp.get_html('https://www.qiushibaike.com/hot/page/3/')
    print html
    m = re.findall(patt_new, html)

    print m


if __name__ == '__main__':
    main()