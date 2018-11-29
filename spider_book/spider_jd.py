import requests
from lxml import html


class GetJDBook(object):

    def __init__(self, isbn):
        self.jd_url = 'https://search.jd.com/Search?keyword={0}&enc=utf-8'.format(isbn)

    def run(self):
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
            print(title[0])
            # 获取链接
            link = li.xpath('div[@class="gl-i-wrap"]/div[@class="p-name"]/a/@href')
            print('http:{0}'.format(link[0]))
            # 获取价格
            now_price = li.xpath('div[@class="gl-i-wrap"]/div[@class="p-price"]/strong/i/text()')
            print("价格：", now_price[0])
            # 获取店铺
            store = li.xpath('div[@class="gl-i-wrap"]/div[@class="p-shopnum"]/a/text()')
            if store == []:
                store.append('当当自营')
            print(store[0])


            print("----------------------------------------")



if __name__ == '__main__':
    # 9787115428028
    # ISBN = input("请输入书籍的isbn: ")
    rest = GetJDBook(9787115428028)
    rest.run()
