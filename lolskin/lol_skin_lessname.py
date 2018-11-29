import requests
from lxml import html
import os
import json


class GetLolSkin(object):
    def __init__(self):
        """类初始化"""
        self.base_url = 'https://lol.qq.com/data/info-defail.shtml?id='
        # 英雄列表的json数据url
        self.hero_list_json_url = 'https://lol.qq.com/biz/hero/champion.js'
        # 每一个英雄的详细资料js文件url
        self.hero_js_url = 'http://lol.qq.com/biz/hero/'
        # 图片前缀url
        self.hero_skin_img_prefix_url = 'https://ossweb-img.qq.com/images/lol/web201310/skin/big'
        # 图片后缀url
        self.hero_skin_img_postfix_url = ''
        # 图片文件夹名称
        self.img_file = 'skin-num'

    def create_img_file(self):
        """创建图片存储文件夹"""
        if not os.path.exists(self.img_file):
            os.mkdir(self.img_file)

    def get_html_str(self, url):
        """下载html"""
        response = requests.get(url)
        response.encoding = 'gbk'
        if response.status_code == 200:
            return response.text
        else:
            return "{}"

    def get_hero_json(self):
        """获取英雄列表的json数据"""
        # 首先获取到js文件
        hero_list_str = self.get_html_str(self.hero_list_json_url)
        # 删除左右多余数据得到json数据
        str_left = "if(!LOLherojs)var LOLherojs={};LOLherojs.champion="
        str_right = ";"
        # replace是替换掉参数中的数据， rstrip是删除末尾的指定字符
        hero_json_str= hero_list_str.replace(str_left, '').rstrip(str_right)
        # print(hero_json_str)
        return json.loads(hero_json_str)

    def get_hero_info(self, hero_id):
        """获取每一个英雄的详细json数据"""
        hero_js_deatil_url = self.hero_js_url + hero_id + '.js'
        hero_list_detail_str = self.get_html_str(hero_js_deatil_url)
        # 删除左右多余数据得到json数据
        detail_str_left = "if(!herojs)var herojs={champion:{}};herojs['champion'][%s]=" % hero_id
        detail_str_right = ";"
        # print(type(hero_list_detail_str))
        hero_detail_json_str = hero_list_detail_str.replace(detail_str_left, '').rstrip(detail_str_right)
        return json.loads(hero_detail_json_str)

    def download_skin_list(self, skin_list, hero_name):
        """"下载皮肤列表"""
        # 循环下载皮肤
        for skin_info in skin_list:
            if skin_info['name'] == 'default':
                skin_name = '默认皮肤'
            else:
                skin_name = skin_info['name']
            hero_skin_name = hero_name + '-' + skin_name + '.jpg'
            if skin_info == skin_list[-1]:
                last_skin = 1
            else:
                last_skin = 0
            self.download_skin(skin_info['id'], hero_skin_name, last_skin)

    def download_skin(self, skin_id, skin_name, last_skin):
        """下载皮肤图片"""
        #下载图片
        img_url = self.hero_skin_img_prefix_url + skin_id + '.jpg'

        response = requests.get(img_url)
        if response.status_code == 200:
            print("download....{0}".format(skin_name))
            img_path = os.path.join(self.img_file, skin_name)
            with open(img_path, 'wb') as img:
                img.write(response.content)
            skin_id2 = skin_id
            if last_skin == 1:
                while True:
                    skin_id2 = int(skin_id2) + 1
                    skin_id2 = str(skin_id2)
                    img_url2 = self.hero_skin_img_prefix_url + skin_id2 + '.jpg'
                    response = requests.get(img_url2)
                    if response.status_code == 200:
                        skin_name2 = skin_id2 + '-' + skin_name
                        print("download....{0}".format(skin_name2))
                        img_path = os.path.join(self.img_file, skin_name2)
                        with open(img_path, 'wb') as img:
                            img.write(response.content)
                    else:
                        break
        else:
            print("img error!")

    def get_bugskin_list(self, hero_ename, hero_id):
        """获取有问题的英雄的皮肤"""
        bug_skin_list = []
        id = 0
        while True:
            if id<10:
                bug_id = hero_id + '00' + str(id)
            else:
                bug_id = hero_id + '0' + str(id)
            img_url = self.hero_skin_img_prefix_url + bug_id + '.jpg'
            response = requests.get(img_url)
            if response.status_code == 404:
                break
            else:
                id = id + 1
                if response.status_code == 200:
                    skin_name = hero_ename + '-' + bug_id + '.jpg'
                    print("download....{0}".format(skin_name))
                    img_path = os.path.join(self.img_file, skin_name)
                    with open(img_path, 'wb') as img:
                        img.write(response.content)
                else:
                    print("img error!")
                # skin_dicts = {'id': bug_id, 'name': bug_id}
                # bug_skin_list.append(skin_dicts)
        # return bug_skin_list


    def run(self):
        """脚本运行入口"""
        self.create_img_file()
        # 获取英雄列表js数据
        hero_json = self.get_hero_json()
        hero_keys = hero_json['keys']
        # 通过循环取出字典的键与值
        # 循环一次就是一个英雄，即遍历每一个英雄
        for hero_id, hero_ename in hero_keys.items():
            hero_name = hero_json['data'][hero_ename]['name']
            detail_json_list = self.get_hero_info(hero_id)
            # 判断数据是否为空
            if detail_json_list:
                skin_list = detail_json_list['result'][hero_id]['skins']
                # 下载皮肤
                self.download_skin_list(skin_list, hero_name)
            else:
                print("英雄:{0}的皮肤获取有问题".format(hero_name))
                bugskin_list = self.get_bugskin_list(hero_ename, hero_id)
                # 下载皮肤
                # self.download_skin_list(bugskin_list, hero_name)







if __name__ == '__main__':
    lol = GetLolSkin()
    lol.run()