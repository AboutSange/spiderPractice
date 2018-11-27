#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
爬取百度贴吧
1.输入帖子代号，以帖子名保存到本地
2.是否只看楼主
"""


import os
import re
import sys
import codecs
import urllib
import urllib2

reload(sys)
sys.setdefaultencoding('utf-8')


# 处理页面标签类
class Tool(object):
    # 去除img标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换为\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD= re.compile('<td>')
    # 把段落开头换为\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n    ", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        # strip()将前后多余内容删除
        return x.strip()

    def replace_title(self, title):
        remove_char_list = ['\\', '/', ':', '*', '?', '"', '<', '>', '|']  # windows文件名不支持的字符
        for ch in remove_char_list:
            title = title.replace(ch, '_')

        return title


class BDTB(object):
    def __init__(self, post_id, see_lz, save_dir):
        """
        :param str post_id: 帖子ID
        :param str see_lz: 只看楼主。0：不只看楼主； 1：只看楼主
        """
        post_id = str(post_id)
        see_lz = str(see_lz)
        self.save_dir = save_dir

        self.page_num = 0
        self.base_url = r'https://tieba.baidu.com/p/{post_id}?see_lz={see_lz}'.format(
            post_id=post_id,
            see_lz=see_lz,
        )

        self.title = '默认标题'
        self.total_page_num = 1  # 总页数

        patt = r'class="p_author_name.*?j_user_card".*?>(.*?)</a>(?#楼层作者)' \
               '.*?' \
               'class="d_post_content j_d_post_content ".*?>(.*?)</div>(?#楼层内容)' \
               '.*?' \
               '<span class="tail-info">(\d+楼)</span><span class="tail-info">(.*?)</span></div>(?#楼层和发表时间)'
        self.patt = re.compile(patt, re.S)  # re.S: make dot match newline

        self.tool = Tool()

    def generate_url(self):
        """生成一个待抓取的URL
        :return: 待抓取的URL
        :rtype: str
        """
        self.page_num += 1
        return '{0}&pn={1}'.format(self.base_url, self.page_num)

    def get_html(self, url):
        try:
            response = urllib2.urlopen(url, timeout=6)
            result = response.read()
        except Exception as e:
            print e
            result = None

        return result

    def get_title_and_total_page_num(self, html):
        """获取标题和总页数"""
        patt = 'class="core_title_txt pull-left text-overflow.*?>(.*?)</h3>.*?<span class="red">(.*?)</span>'
        m = re.search(patt, html, re.S)
        if m is not None:
            self.title = self.tool.replace_title(m.group(1))
            self.total_page_num = int(m.group(2))
        else:
            print '[error]search title error'

    def parse_html(self, html):
        """解析HTML
        :return: [楼层1, 楼层2]  ；楼层1：(楼层作者，楼层内容，楼层, 发表时间)
        :rtype: list<tuple>
        """
        m = re.findall(self.patt, html)
        return m

    def write_file(self, floor_list):
        """将floor_list内容写入文件中去
        :param list floor_list: [楼层1, 楼层2]  ；楼层1：(楼层作者，楼层内容，楼层, 发表时间)
        """
        #
        save_file_path = os.path.join(self.save_dir, r'{0}.txt'.format(self.title.decode('utf-8').encode(sys.getfilesystemencoding())))
        if os.path.exists(save_file_path):
            write_type = 'a'
        else:
            write_type = 'w'

        with codecs.open(save_file_path, write_type, 'utf-8') as f:

            for floor in floor_list:
                author = floor[0]
                content = self.tool.replace(floor[1])
                floor_num = floor[2]
                write_date = floor[3]

                f.write('=' * 20)
                f.write('\n\n')
                f.write('楼层：{0}\n'.format(floor_num))
                f.write('楼层作者：{0}\n'.format(author))
                f.write('发表时间：{0}\n'.format(write_date))
                f.write('楼层内容：{0}\n'.format(content))
                f.write('\n')
                f.write('=' * 20)

    def run(self):
        have_title = False
        while self.page_num < self.total_page_num:
            url = self.generate_url()  # self.page_num += 1
            html = self.get_html(url)
            if not have_title:
                self.get_title_and_total_page_num(html)  # self.total_page_num
                print self.title
                print '该帖子共有{0}页'.format(self.total_page_num)
                have_title = True
            floor_list = self.parse_html(html)
            print '正在写入第{0}页数据'.format(self.page_num)
            self.write_file(floor_list)

        print '写入任务完成'


def main():
    # 3138733512
    obj = BDTB(post_id='5912337021', see_lz='0', save_dir=r'E:\Test')
    obj.run()


if __name__ == '__main__':
    main()
