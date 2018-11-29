# D:\pycharm2\PyCharm 2018.2.4\projects\Skin
# 第一步：定义初始化一些变量，例如url
# 第二步：抓取所有英雄的列表
# 第三步：循环遍历，分析每一个英雄皮肤的节点
# 第四步：下载图片
# 第五步：爬虫结束
import time
import requests
# 获取HTML中的节点信息
from bs4 import BeautifulSoup
# url的拼接parse.urljoin(url1, url2)
from urllib import parse
import os
# from lxml import html


class Skin(object):

    def __init__(self):
        """初始化url"""
        # 英雄的json数据url
        self.hero_json_url = 'https://pvp.qq.com/web201605/js/herolist.json'
        # 英雄详细页的前缀url
        self.hero_prefix_url = 'https://pvp.qq.com/web201605/herodetail/'
        # 英雄详细页的url后缀信息
        self.hero_detail_url = ''
        # 英雄皮肤图片的前缀url,记得以https://开头
        self.skin_img_prefix_url = 'https://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/'
        # 英雄皮肤图片的url后缀信息
        self.skin_img_detail_url = ''
        # 图片储存文件夹
        self.img_folder = 'skin'

    def run(self):
        """脚本执行入口"""
        # 函数创建图片存储文件夹
        self.make_folder()
        # 函数获取英雄列表的json数据
        hero_list = self.get_hero_json()
        # 通过使用for循环下载英雄列表里面皮肤的图片
        for hero in hero_list:
            hero_num = str(hero['ename'])  # for循环遍历获取英雄编号和英雄名字
            self.hero_detail_url = '{0}.shtml'.format(hero_num)  # 并组合成英雄详细页的url后缀信息
            hero_name = hero['cname']  # 获取英雄名字
            self.get_hero_skin(hero_name, hero_num)
            # 函数获取详细页英雄皮肤展示的信息，并下载皮肤图片

        # 函数参数为英雄编号和英雄名字

    def make_folder(self):
        """函数创建图片存储文件夹"""
        if not os.path.exists(self.img_folder):
            os.mkdir(self.img_folder)

    def get_hero_json(self):
        """函数获取英雄列表的json数据"""
        request = requests.get(self.hero_json_url)
        hero_list = request.json()
        return hero_list

    def get_hero_skin(self, hero_name, hero_num):
        """函数获取详细页英雄皮肤展示的信息，并下载图片"""
        # 合并英雄详细页的url
        url = parse.urljoin(self.hero_prefix_url, self.hero_detail_url)
        # 获取英雄详细页的请求响应request = requests(url)
        request = requests.get(url)
        # 设置请求的编码格式为gbk
        request.encoding = 'gbk'
        # 获取页面html的text文件即字符串
        html_str = request.text
        # 获取皮肤信息的节点
        # 使用Beautifulsoup(html,'lxml')获取html页面的对象，html为请求文本
        soup = BeautifulSoup(html_str,'lxml')
        # 然后soup对象调用select(目标标签)返回目标标签列表
        skip_list = soup.select('.pic-pf-list3')
        # for获取皮肤名称
        for skin_info in skip_list:
            skin_img_name = skin_info.attrs['data-imgname']  # 标签.attrs['data-imgname']返回该标签属性为data-imgname的属性值即图片名称
            name_list = skin_img_name.split('|')  # 把名称字符串去除'|'放到名称列表
            skin_num = 1  # 并初始化皮肤编号为1
            for skin_name in name_list:  # for循环下载皮肤图片，参数为图片名字循环参数为皮肤名字
                self.skin_img_detail_url = '{0}/{0}-bigskin-{1}.jpg'.format(hero_num, skin_num)
                skin_num += 1  # 完善英雄皮肤图片的url后缀信息，并皮肤编号自加1
                # img_name = hero_name + '-' +skin_name + '.jpg'
                img_name = '{0}-{1}.jpg'.format(hero_name, skin_name)
                # 设图片名字为hero_name-skin_name.jpg
                self.download_skin_img(img_name)
                # 调用下载函数参数为图片名字

    def download_skin_img(self, img_name):
        """函数下载图片,参数为图片名字"""
        # 合并英雄皮肤图片的url
        img_url = parse.urljoin(self.skin_img_prefix_url, self.skin_img_detail_url)
        # 通过英雄图片的url获取请求响应request = requests(url)
        request = requests.get(img_url)

        # 通过判断HTTP编码是否是200判断请求成不成功
        if request.status_code == 200:
            print('download-{0}'.format(img_name))  # 成功输出download-图片名字
            img_path = os.path.join(self.img_folder, img_name)  # 并合并出图片路径(图片文件夹+图片名字)
            with open(img_path, 'wb') as img:  # 以wb的形式打开图片路径获得文件对象，文件对象调用write(request.content)
                img.write(request.content)
            # 躲避反爬措施
            time.sleep(1)
        else:
            print("img error！")  # 失败输出img error！


if __name__ == '__main__':
    skin = Skin()
    skin.run()

