from typing import NamedTuple
import requests
from lxml import html


class BookObject(NamedTuple):
    title: str
    price: float
    link: str
    store: str

    def __str__(self):
        return '价格: {self.price}， 名称: {self.title}, 链接：{self.link}, 店铺：{self.store}'.format(self=self)


class Spider_Book(object):
    def __init__(self, sn):
        self.sn = sn
        self.book_list = []

    def spider_dangdang(self):
        self.dd_url = 'http://search.dangdang.com/?key={isbn}&act=input'.format(isbn = self.sn)
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
            # 获取链接
            link = li.xpath('p[@class="name"]/a/@href')
            # 获取价格
            now_price = li.xpath('p[@class="price"]/span[@class="search_now_price"]/text()')
            if len(now_price) == 0:
                now_price_bug = li.xpath('div[@class="ebook_buy"]/p/span[@class="search_now_price"]/text()')
                now_price = now_price_bug
            # 获取店铺
            store = li.xpath('p[@class="search_shangjia"]/a[@name="itemlist-shop-name"]/text()')
            if store == []:
                store.append('当当自营')
            book = BookObject(
                title= title[0],
                price= now_price[0].replace('¥', ''),
                link= link[0],
                store= store[0]
            )
            self.book_list.append(book)
    def spider_jd(self):
        self.jd_url = 'https://search.jd.com/Search?keyword={isbn}&enc=utf-8'.format(isbn = self.sn)
        # 获取html文本
        respones = requests.get(self.jd_url)
        respones.encoding = 'utf-8'
        html_str = respones.text
        # 使用lxml获取html元素对象
        selector = html.fromstring(html_str)
        # 对象调用xpath()获取标签内容
        ul_list = selector.xpath('//div[@id="J_goodsList"]/ul/li')
        # print(len(ul_list))
        for li in ul_list:
            # 获取名字
            title = li.xpath('div[@class="gl-i-wrap"]/div[@class="p-name"]/a/em/text()')
            # 获取链接
            link = li.xpath('div[@class="gl-i-wrap"]/div[@class="p-name"]/a/@href')
            link[0] = 'http:{0}'.format(link[0])
            # 获取价格
            now_price = li.xpath('div[@class="gl-i-wrap"]/div[@class="p-price"]/strong/i/text()')
            # 获取店铺
            store = li.xpath('div[@class="gl-i-wrap"]/div[@class="p-shopnum"]/a/text()')
            if store == []:
                store.append('京东自营')
            book = BookObject(
                title=title[0],
                price=now_price[0].replace('¥', ''),
                link=link[0],
                store=store[0]
            )
            self.book_list.append(book)
    def spider_yhd(self):
        self.yhd_url = 'https://search.yhd.com/c0-0/k{isbn}/'.format(isbn = self.sn)
        # 获取html文本
        respones = requests.get(self.yhd_url)
        html_str = respones.text
        # 使用lxml获取html元素对象
        selector = html.fromstring(html_str)
        # 对象调用xpath()获取标签内容
        ul_list = selector.xpath('//div[@id="itemSearchList"]/div')
        for li in ul_list:
            # 获取名字
            title = li.xpath('div/p[@class="proName clearfix"]/a/@title')
            # 获取链接
            link = li.xpath('div/p[@class="proName clearfix"]/a/@href')
            link[0] = 'http:{0}'.format(link[0])
            # 获取价格
            now_price = li.xpath('div/p[@class="proPrice"]/em/@yhdprice')
            # 获取店铺
            store = li.xpath('div/p[@class="storeName limit_width"]/a/text()')
            if store == []:
                store.append('1号店自营')
            else:
                store[0] = store[0].replace('\n', '')
            book = BookObject(
                title=title[0],
                price=now_price[0].replace('¥', ''),
                link=link[0],
                store=store[0]
            )
            self.book_list.append(book)
    def sorted_price(self):
        self.spider_dangdang()
        self.spider_jd()
        self.spider_yhd()
        sorted_book_list = sorted(self.book_list, key=lambda item: float(item.price), reverse=True)
        print('>>>>>>>>>', len(sorted_book_list))
        for book in sorted_book_list:
            print(book)


if __name__ == '__main__':
    # 9787115428028
    ISBN = input("请输入要查找图书的ISBN编码:")
    rest = Spider_Book(ISBN)
    rest.sorted_price()