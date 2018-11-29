import requests
from lxml import html


class GetYHDBook(object):

    def __init__(self, isbn):
        self.yhd_url = 'https://search.yhd.com/c0-0/k{0}/'.format(isbn)

    def run(self):
        # 获取html文本
        respones = requests.get(self.yhd_url)
        # respones.encoding = 'utf-8'
        html_str = respones.text
        # 使用lxml获取html元素对象
        selector = html.fromstring(html_str)
        # 对象调用xpath()获取标签内容
        ul_list = selector.xpath('//div[@id="itemSearchList"]/div')
        # print(len(ul_list))
        for li in ul_list:
            # 获取名字
            title = li.xpath('div/p[@class="proName clearfix"]/a/@title')
            print(title[0])
            # 获取链接
            link = li.xpath('div/p[@class="proName clearfix"]/a/@href')
            print('http:{0}'.format(link[0]))
            # 获取价格
            now_price = li.xpath('div/p[@class="proPrice"]/em/@yhdprice')
            print("价格：", now_price[0])
            # 获取店铺
            store = li.xpath('div/p[@class="storeName limit_width"]/a/text()')
            print('1号店自营' if store == [] else store[0])


            # print("----------------------------------------")



if __name__ == '__main__':
    # 9787115428028
    # ISBN = input("请输入书籍的isbn: ")
    rest = GetYHDBook(9787115428028)
    rest.run()
