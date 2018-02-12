
import hashlib
import base64
import time
import requests
from urllib.parse import parse_qs, urlparse



AUTHORIZATION_SIFFOX = "6e8566e348447383e16fdd1b233dbb49"
AUTHORIZATION_PREFIX = 'ljwxapp:'

def dict_sort(d):
    return {k: d[k] for k in sorted(d)}


def get_authorization(data):"""
    
    获取 authorization
    :param data: 
    例子参数
    {'city_id': '310000', 'condition': '', 'query': '', 'order': '', 'offset': '0', 'limit': '10', 'sign': ''}
    :return: 
    例子 authorization 返回值
    b'bGp3eGFwcDoxYmU3OThjZDg0ZWU4NzNmM2JhMzM0NTFhZTNkNWUwMA=='
    """

    global AUTHORIZATION_SIFFOX
    global AUTHORIZATION_PREFIX
    l = ""
    data_sort = dict_sort(data)
    l += ''.join([key + '=' + str(data_sort[key]) for key in data_sort.keys()])
    l += AUTHORIZATION_SIFFOX
    l_md5 = hashlib.md5(l.encode()).hexdigest()
    authorization_source = AUTHORIZATION_PREFIX+l_md5
    authorization = base64.b64encode(authorization_source.encode())

    return authorization.decode()


def get_house_list(url):
    parse = parse_qs(urlparse(url).query, keep_blank_values=True)
    data = {key: value[-1] for key, value in parse.items()}

    authorization = get_authorization(data)

    headers = {
        'Lianjia-Uuid': '4fbaf7cccaa68133621280c523aada66',
        'Wxminiapp-SDK-Version': '1.9.9',
        'Lianjia-Wxminiapp-Version': '0.1',
        'Authorization': '',
        'Accept': '*/*',
        'Lianjia-Source': 'ljwxapp',
        'Time-Stamp': str(int(time.time() * 1000)),
        'Accept-Language': 'zh-cn',
        'Lianjia-Session': '',
        'Accept-Encoding': 'gzip, deflate',
        'Wx-Version': '6.6.1',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 MicroMessenger/6.6.1 NetType/WIFI Language/zh_CN',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'OS-Version': 'ios-iOS 10.3.3',
    }

    headers['Authorization'] = authorization
    r = requests.get(url, headers=headers)
    return r.json()

def quest_str():

    # 获取二手房数据列表
    get_ershoufang_url = {
        'url': 'https://wechat.lianjia.com/ershoufang/search?city_id=310000&condition=&query=&order=&offset=0&limit=10&sign='
    }

    """
    获取二手房数据列表
    'url': 'https://wechat.lianjia.com/ershoufang/search?city_id=310000&condition=&query=&order=&offset=0&limit=10&sign='
    
    获取房源详细信息
    'url': 'https://wechat.lianjia.com/ershoufang/detail?house_code=107001753941&sign=',
    
    获取小区数据
    https://wechat.lianjia.com/ershoufang/xiaoqu?resblock_id=5011000018313&sign=
    
    获取推荐数据
    https://wechat.lianjia.com/ershoufang/recommend?city_id=310000&house_code=107001753941&sign=
    
    """

    city_id = {

        'sh': '310000',
        'sz': '440300',
        'tj': '120000',
        'bj': '110000',
        'gz': '440100',
        'fs': '440600',
    }


if __name__ in "__main__":
    # 获取上海 二手房数据
    url = 'https://wechat.lianjia.com/ershoufang/search?city_id=310000&condition=&query=&order=&offset=0&limit=10&sign='

    # 读取 100条数据
    for p in range(0,100,10):
        url_1 = 'https://wechat.lianjia.com/ershoufang/search?city_id=310000&condition=&query=&order=&offset={}&limit=10&sign='.format(p)
        jj = get_house_list(url_1)
        print(jj['data'])


