#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
爬取糗事百科
    1.抓取糗事百科热门段子（https://www.qiushibaike.com/hot/page/2/）
    2.过滤带有图片的段子
    3.实现每按一次回车显示一个段子的发布人，段子内容，好笑数。
    4.时刻保持缓存20个段子或以上
"""

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


class QSBK(object):
    def __init__(self):
        self.spider = Spider()

        self.url_root = r'https://www.qiushibaike.com/hot/page/'
        self.index = 0

        self.joke_list = []  # 段子列表

        # (?#注释内容)
        patt = r'class="article block untagged mb15(?#识别到段子div块)' \
               r'.*?' \
               r'class="author clearfix"(?#识别到作者信息（头像、昵称、等级）div块)' \
               r'.*?' \
               r'<h2>(?P<joke_author>.*?)</h2>(?#作者昵称)' \
               r'.*?' \
               r'class="content".*?<span>(?P<joke_content>.*?)</span>(?#段子内容)' \
               r'.*?' \
               r'class="stats-vote"><i class="number">(?P<joke_like_num>.*?)</i>(?#段子好笑数)'
        self.patt = re.compile(patt, re.S)  # 注意设置.可以表示换行符，因为在joke_content中需要

    def generate_url(self):
        """生成一个待抓取的URL
        :return: 待抓取的URL
        :rtype: str
        """
        self.index += 1
        return '{0}{1}/'.format(self.url_root, self.index)

    def get_html(self, url):
        """获取URL的HTML
        :return: HTML
        :rtype: str
        """
        return self.spider.get_html(url)

    def parse_html(self, html):
        """解析HTML
        :return: [段子1, 段子2]  ；段子1：(发布人，段子内容，好笑数)
        :rtype: list<tuple>
        """
        joke_list = []
        m = re.findall(self.patt, html)
        return m

    def show_joke(self):
        """显示段子"""
        if self.joke_list:
            joke = self.joke_list.pop(0)  # [发布人，段子内容，好笑数]
            joke_author = joke[0].strip()  # 发布人
            joke_content = joke[1].replace('<br/>', '\n').strip()  # 段子内容
            joke_like_num = joke[2].strip()  # 好笑数（点赞数）
            print '=' * 20
            print
            print '发布人：{0}'.format(joke_author)
            print '段子内容：{0}'.format(joke_content)
            print '好笑数：{0}'.format(joke_like_num)
            print
            print '=' * 20
        else:
            print '=' * 20
            print
            print '没有段子了！'
            print
            print '=' * 20

    def run(self):
        """开始展示"""
        while True:
            while len(self.joke_list) < 20:
                url = self.generate_url()  # 生成一个新URL
                html = self.get_html(url)  # 获取该URL的HTML
                new_joke_list = self.parse_html(html)  # 解析HTML得到该URL的段子列表
                self.joke_list.extend(new_joke_list)  # 加入到全局段子列表中

            print '**********已加载到第{0}页'.format(self.index)
            print '**********已缓存的段子数 {0}'.format(len(self.joke_list))
            self.show_joke()  # 显示一个段子: [发布人，段子内容，好笑数]
            input_str = raw_input('按回车继续，按q/Q退出')
            if input_str.lower() == 'q':
                break


def main():
    qsbk = QSBK()
    qsbk.run()


if __name__ == '__main__':
    main()
