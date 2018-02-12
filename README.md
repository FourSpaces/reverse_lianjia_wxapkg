# reverse_lianjia_wxapkg
逆向链家微信小程序，解析 请求的加密方式获取数据

### 破解链家小程序中的请求加密方式：
- 1、获取链家微信小程序的 .wxapkg 包文件、解开 .wxapkg 程序包
- 2、了解.wxapkg文件结构
- 3、查看程序逻辑，实验生成Authorization
- 4、验证迭代、实现加密方式

详细破解过程见我的 知乎文章。

### Authorization 生成方式：
这里以获取二手房信息为例

Url = 'https://wechat.lianjia.com/ershoufang/search?city_id=310000&condition=&query=&order=&offset=0&limit=10&sign='

Authorization = 'bGp3eGFwcDoxYmU3OThjZDg0ZWU4NzNmM2JhMzM0NTFhZTNkNWUwMA=='

加密过程

1、获取参数部分，这里为 ‘city=310000&condition=&query=&order=&offset=0&limit=10&sign=’

2、对参数进行从大到小排序、并将key-value用等号连接起来，将所有的元素连接成为一个字符串 S

      排序后：

           {'city_id': '310000', 'condition': '', 'limit': '10', 'offset': '0', 'order': '', 'query': '', 'sign': ''}

      key-value用等号连接起来，并连接所有元素：

           S =  'city_id=310000condition=limit=10offset=0order=query=sign='

3、 添加后缀 "6e8566e348447383e16fdd1b233dbb49"到变量S中，获取S的MD5值。

4、为变量 S 的MD5值 添加前缀 ‘ljwxapp:’，并作base64 编码，生成为：‘bGp3eGFwcDoxYmU3OThjZDg0ZWU4NzNmM2JhMzM0NTFhZTNkNWUwMA==’的 Authorization



Python 实现代码如下

    AUTHORIZATION_SIFFOX = "6e8566e348447383e16fdd1b233dbb49"
    AUTHORIZATION_PREFIX = 'ljwxapp:'
    
    def get_authorization(data):
    	"""    
        获取 authorization
        :param data: 
        	例子参数
            {'city_id': '310000', 'condition': '', 'query': '', 'order': '', 
            'offset': '0', 'limit': '10', 'sign': ''}
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

更详细的见代码部分见 [wxlj_Authorization_test.py](https://github.com/Ant-Ferry/reverse_lianjia_wxapkg/blob/master/wxlj_Authorization_test.py)，
其中实现了一个 获取上海 二手房数据列表的例子。


