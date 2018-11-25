import requests
import json
import datetime
import random

ip_random = -1


def get_html(url):
    """获取html"""
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    }
    global ip_random
    ip_rand, proxies = get_proxy(ip_random)
    try:
        response = requests.get(url, headers=header, proxies=proxies, timeout=3)
    except:
        request_status = 500
    else:
        request_status = response.status_code
    print("request_status:", request_status)
    if request_status == 200:
        print("ip可用")
    else:
        print("ip不可用")

    while request_status !=200:
        ip_random = -1
        ip_rand, proxies = get_proxy(ip_random)
        try:
            response = requests.get(url, headers=header, proxies=proxies, timeout=3)
        except:
            request_status = 500
        else:
            request_status = response.status_code
            print("request_status:", request_status)
            if request_status == 200:
                print("ip可用")
            else:
                print("ip不可用")
    ip_random = ip_rand
    html_str = response.text
    return html_str



def get_proxy(random_number):
    """获取设置代理的字典"""
    with open('ip.txt', 'r') as fail:
        ip_list = json.load(fail)
    if random_number == -1:
        random_number = random.randint(0,len(ip_list)-1)
    ip_info = ip_list[random_number]
    ip_address_port = '://' + ip_info['address'] + ':' + ip_info['port']
    proxies_dict = {
        'http': 'http' + ip_address_port,
        'https': 'https' + ip_address_port
    }
    print(proxies_dict)
    return random_number, proxies_dict


if __name__ == '__main__':
    # 程序的主入口
    start_time = datetime.datetime.now()
    url = "https://book.douban.com/tag/?view=type&icn=index-sorttags-all"
    html_str = get_html(url)