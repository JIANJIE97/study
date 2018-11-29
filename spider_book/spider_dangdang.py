import requests
from lxml import html


class GetDDBook(object):

    def __init__(self, isbn):
        self.dd_url = 'http://search.dangdang.com/?key={0}&act=input'.format(isbn)

    def run(self):
        # 获取html文本
        respones = requests.get(self.dd_url)
        html_str = respones.text
        # 使用lxml获取html元素对象
        selector = html.fromstring(html_str)
        # 对象调用xpath()获取标签内容
        ul_list = selector.xpath('//div[@id="search_nature_rg"]/ul/li')
        for li in ul_list:
            # 获取名字
            title = li.xpath('p[@class="name"]/a/@title')
            print(title[0])
            # 获取链接
            link = li.xpath('p[@class="name"]/a/@href')
            print(link[0])
            # 获取价格
            now_price = li.xpath('p[@class="price"]/span[@class="search_now_price"]/text()')
            if len(now_price) == 0:
                now_price_bug = li.xpath('div[@class="ebook_buy"]/p/span[@class="search_now_price"]/text()')
                print("该商品无折扣，价格：", now_price_bug[0].replace('¥', ''))
            else:
                print("折后价：", now_price[0].replace('¥', ''))
            pre_price = li.xpath('p[@class="price"]/span[@class="search_pre_price"]/text()')
            if len(pre_price) == 0:
                pre_price_bug = li.xpath('div[@class="ebook_buy"]/p/span[@class="search_now_price"]/text()')
                # print("该商品无折扣，价格：", pre_price_bug[0].replace('¥', ''))
            else:
                print("原价：", pre_price[0].replace('¥', ''))
            # 获取店铺
            store = li.xpath('p[@class="search_shangjia"]/a[@name="itemlist-shop-name"]/text()')
            print('当当自营' if store == [] else store[0])

            print("----------------------------------------")


if __name__ == '__main__':
    # 9787115428028
    # ISBN = input("请输入书籍的isbn: ")
    rest = GetDDBook(9787115428028)
    rest.run()
