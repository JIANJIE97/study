# D:\pycharm\PyCharm 2018.2.5\projects\spider_main
# 1、爬取一些IP,过滤掉不可用.
# 2、在requests的请求的proxies参数加入对应的IP.
# 3、继续爬取.
# 使用urllib库获取HTML需要
# 1、proxy_dicy = {
#     'http':'http://192.168.1.1:8080',
#     'https':'https://192.168.1.1:8080',
# }
# 2、proxy_handler = urllib.request.ProxyHandler(proxy_dict)
# 3、operen = urllib.request.build_opener(proxy_handler)
# 4、urllib,request.install_opener(opener)
# 5、request = urllib.request.Request(url,headers=headers)
# 6、response = urllib.request.urlopen(request)
# 7、response.read().decode('utf-8')
import requests
from lxml import html
import json
import urllib.request
from urllib import error


class SpiderIp(object):
    def __init__(self):
        """变量初始化"""
        self.url = "http://www.xicidaili.com/nn/"
        self.ip_test_url = "https://www.ip.cn/"
        self.ip_list = []

    def get_html(self):
        """获取HTML源代码"""
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        try:
            # 使用requests库请求HTML
            response = requests.get(self.url, headers=header)
            response.encoding = 'utf-8'
            html_str = response.text
            return html_str
        except Exception as e:
            return ''

    def get_bool_ip(self, ip_address, ip_port):
        """验证IP地址是否可用"""
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        ip_proxy_url = '://' + ip_address + ':' + ip_port
        proxies = {
            'http': 'http' + ip_proxy_url,
            'https': 'https' + ip_proxy_url
        }
        # 使用urllib库中的ProxyHandler方法为请求设置代理返回一个handler
        proxy_handler = urllib.request.ProxyHandler(proxies)
        try:
            # print("调试")
            # 使用requests库请求HTML
            # response = requests.get(self.ip_test_url, headers=header, proxies=proxies, timeout=3)
            # html_str = response.text
            # 使用urllib库请求HTML
            # 使用build_opener(handler)方法来创建opener对象
            opener = urllib.request.build_opener(proxy_handler)
            # 使用install_opener(opener)方法创建自定义的opener
            urllib.request.install_opener(opener)
            # 使用Request类来构建一个请求
            request = urllib.request.Request(self.ip_test_url, headers=header)
            response = urllib.request.urlopen(request, timeout=3)
            # html_str = response.read()
            # print(type(response))
            # <class 'http.client.HTTPResponse'>
            # print(">>>>>>>调试", html_str)
        except :
            print("fail:{0}".format(ip_address))
        # except error.HTTPError as e:
        #     print("-------------------------1")
        #     print(e.reason, e.code, e.headers, sep='\n')
        #     print("fail:{0}".format(ip_address))
        # except error.URLError as e:
        #     print("-------------------------2")
        #     print(e.reason)
        else:
            print("-------------------------")
            print("success:{0}".format(ip_address))
            ip_info = {
                'address': ip_address,
                'port': ip_port
            }
            self.ip_list.append(ip_info)

    def run(self):
        """程序执行入口"""
        html_str = self.get_html()
        selector = html.fromstring(html_str)
        tag_list = selector.xpath('//table[@id="ip_list"]/tr')
        tag_list = tag_list[1:]
        for tag in tag_list:
            ip_address = tag.xpath('td[2]/text()')
            ip_port = tag.xpath('td[3]/text()')
            self.get_bool_ip(ip_address[0], ip_port[0])
        # 写入文件
        # dumps与dump的区别loads与load的区别
        # json.dump(self.ip_list, fail)是把Python的基础类型编码为str并保存到fail
        # str_json = json.dumps(self.ip_list)只是把Python的基础类型编码为str
        # json.loads(str_json)只是把str解码为Python的基础类型
        # json.load(fail)从文件fail中把str解码为Python的基础类型
        with open('ip.txt', 'w') as fail:
            json.dump(self.ip_list, fail)


if __name__ == '__main__':
    spider_ip = SpiderIp()
    spider_ip.run()