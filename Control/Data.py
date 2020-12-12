# -*- coding: UTF-8 -*-
import re
import time
from Control.Config import report_header, header_custom, file_element
from Control.Lib import *
from Control.Log import logger
from Control.Utlis import Excel
from pathlib import Path
from Control.Config import header
import re
import operator
import ast  #可以将字符串转为字典

var = []


def replace(data):
    """这个方法是将自定义函数计算出来,eval函数可以用过字符的方法计算出结果内容，函数嵌套函数也是可以的"""
    # 正则匹配出 data 中所有  中的变量，返回列表 不包含这些内容则返回空
    keys = re.findall(r'<(.*?)>', data)
    # 返回是个list，采用替换的方法进行数据重组
    for r in keys:
        # 第一个参数是原来的值，第二个是参数是计算出来之后得到的值
        data = data.replace('<' + r + '>', str(eval(r)))
    data = data.replace("\n", "")
    # 出现NameError的错误，则认为是上传文件
    return data




def suite2data(data):
    """进行测试报告同步头部标题和内容对应"""
    result = [[header_custom[key.lower()] for key in report_header.values()]]
    for d in data:
        # print("data的值为",data)
        # print("d的值为",d)
        s = d['steps'][0]
        testcase = [d.get('id', 'id'), d.get('title', 'title'), d.get('testdot', 'testdot'), s.get('no', 'no'),
                    s.get('_keyword', '_keyword'), s.get('page', 'page'), s.get('_element', '_element'),
                    s.get('data', 'data'),
                    s.get('output', 'output'),
                    s.get('expected', 'expected'), s.get('assert', 'assert'), d.get('designer', 'designer'),
                    s.get('score', 'score'),
                    s.get('_resultinfo', '')]
        result.append(testcase)

        for s in d['steps'][1:]:
            step = ['', '', s.get('testdot', 'testdot'), s.get('no', 'no'), s.get('_keyword', '_keyword'),
                    s.get('page', 'page'), s.get('_element', '_element'), s.get('data', 'data'),
                    s.get('output', 'output'),
                    s.get('expected', 'expected'), s.get('assert', 'assert'),
                    d.get('designer', 'designer'), s.get('score', 'score'), s.get('_resultinfo', '_resultinfo')]

            result.append(step)

    return result


def gettime():
    nowtime = time.strftime("%Y%m%d_%H%M%S", time.localtime())
    return nowtime


# 处理json类型和参数
def datatating(data):
    #将字符串data转为字典
    data = ast.literal_eval(data)
    # print("=============data的值是",data,type(data))
    d = {}
    #如果data里面没有空格
    if str(data).strip():
        for a in data.items():
            d[str(a[0])] = a[1]
        # print("===============d的值为：",d)
    return d


# # 如果有#号将进行处理，没有不处理
# def affirm(expected):
#     # 返回的是list,只切割一次，切割最后的#号
#     ex_list = str(expected).rsplit('#', 1)
#     # 0代表是预期结果，1是代表是断言的内容
#     # eval处理是元祖类型
#     return ex_list[0], eval(ex_list[1])

#定义断言函数，断言对比
def asset_content(ec_assert, response):
    # logger.info(eval(type(str(ec_assert))))
    # 处理预期结果的内容，切割出来断言
    # 1.是预期结果 2.是需要断言的内容 元祖类型
    fail_tent = ''
    for t in eval(ec_assert):
        # print("===========t的值：",t)
        # print("=============str(response)的值：",str(response))
        if t not in str(response):
            fail_tent += '接口没有此值：%s,' % t
    return fail_tent


def datatodict(data):
    head = []
    list_dict_data = []
    for d in data[1]:
        d = header.get(d, d)
        head.append(d)
    # 获取到数据进行切片处理，0坐标为标题，1坐标是头部
    for b in data[2:]:
        # 头部和内容拼接为json串
        dict_data = {}
        for i in range(len(head)):
            # 之所以判断类型，如果不进行判断会出现str的错误，strip去除空格也有转str的用法
            if isinstance(b[i], str):
                dict_data[head[i]] = b[i].strip()
            else:
                dict_data[head[i]] = b[i]
        # list里面是字典格式
        list_dict_data.append(dict_data)

    return list_dict_data


# dict格式的数据处理为测试套件格式
def suite_format(data):
    from Control.Log import logger
    # 在重组的时候 得到element文件，并制定url

    element = file_element
    # 读取链接和元素表格全部内容
    excel_element = Excel('r', element)
    # 元素和接口转换为json，切片是为了去除表格的第一行
    elements = element_tojson(excel_element.read()[2:])
    testsuite = []
    # 每个用例的testcase
    testcase = {}
    for d in data:
        if d['id'].strip():
            # 判断是否为空 true false
            if testcase:
                testsuite.append(testcase)
                testcase = {}
            # 这里生成了用例的标题行，里面没有step
            for key in ('id', 'title', 'condition', 'testdot', 'designer', 'remark'):
                testcase[key] = d[key]
            testcase['steps'] = []
        no = str(d['step']).strip()
        # 查看是否存在步骤
        if no:
            step = {}
            # 判断步骤里面是否存在这些东西
            # 等于当前步骤
            step['no'] = str(int(d['step']))
            #     去除这些对应的内容放入step里面
            for key in ('testdot', 'keyword', 'element', 'data', 'expected', 'assert', 'output', 'score', 'remark'):
                # 是element直接添加类型
                if key == 'element':
                    # 里面装载 请求的类型 和url 字典格式
                    step[key] = {'type': elements[d.get(key, '')]['type'],
                                 'url': elements['baseurl']['url'] + elements[d.get(key, '')]['url']}
                else:
                    # 获取用例内容字段进行拼接
                    step[key] = d.get(key, '')

                # 仅作为测试结果输出时，保持原样
            for v in ('keyword', 'element', 'data', 'expected', 'assert'):
                step['_{}'.format(v)] = d[v]

            step['resultinfo'] = ''
            # 添加测试步骤
        testcase['steps'].append(step)
        # 不为空则添加到list里面
    if testcase:
        testsuite.append(testcase)
    logger.info(testsuite)
    return testsuite


# 将元素和链接表处理为json格式方便进行查询
def element_tojson(element):
    # 推导式写法
    return {str(e[0]).replace('\n', ''): {'type': e[1],'headers':e[2],'url': e[3]} for e in element}


# 写入token
def writetoken(token):
    path = Path('Control/book') / ('txt_final.txt')
    # 方法可以写入token和普通常量
    f = open(path, 'a')
    f.write(token)
    f.close()


def compare_key_value(json_p):
    list_key = []

    def getkey_value_all(input_json={}):

        if isinstance(input_json, dict):  # isinstance() 函数来判断一个对象是否是一个已知的类型

            for key in input_json.keys():  # keys() 函数以列表返回一个字典所有的键。

                key_value = input_json.get(key)  # get() 函数返回指定键的值，如果值不在字典中返回默认值。

                if isinstance(key_value, dict):  # dict字典

                    getkey_value_all(key_value)

                elif isinstance(key_value, list):

                    for json_array in key_value:
                        getkey_value_all(json_array)

                else:
                    # 对象下面的key
                    list_key.append(str(key))
                    pass
            # 对象类型的key
            # list_key.append(str(key))
        elif isinstance(input_json, list):

            for input_json_array in input_json:
                getkey_value_all(input_json_array)

    getkey_value_all(json_p)
    return list_key


def iscompare_json(sub, parent):
    a1 = compare_key_value(sub)
    a2 = compare_key_value(parent)
    #如果a1等于a2 ，则返回True ，否则返回False
    flag = operator.eq(a1, a2)
    if flag == True:
        return 'Pass'
    else:
        return 'Fail'


def rplaceto_tf(e, r):
    e = eval(str(e).replace('true', 'True').replace('false', 'False').replace('null', 'None'))
    r = eval(str(r).replace('true', 'True').replace('false', 'False').replace('null', 'None'))

    return e, r


# 正则提取json内容的方法
# def extract(keys, values):
#     dict_data = {}
#     for k in keys:
#         regex = r"'%s': '([\s\S]+?)'" % k
#         # 匹配出来是个list
#         match_obj = re.findall(regex, str(content))
#         dict_data[k] = match_obj
#         # 匹配出来字段拼成一个list返回，list里面包含2个内容，第一个内容是key，第二个内容是value一一对应
#     print(dict_data)
#     return keys, values


"""
第一个参数：上个接口的返回值
第二个参数：当前接口的请求测试数据
用来替换测试数据，关联上一个步骤
如果当前content里面没有^这个符号，则直接返回不走下面的方法

从上个接口里面去拿值，拿不到就去整个用例里面去拿
"""


def acquire(last_content, this_content, all_content):
    # 使用正则去里面寻找带^特殊符号开头的内容
    pattern = re.compile(r"'\^([\s\S]+?)'")
    # 拿到匹配的内容 是上个接口的key值
    keys = re.findall(pattern, str(this_content))
    # print(len(keys))
    if len(keys) <= 0:
        return this_content
    # 承载当前匹配出来的内容
    present = []
    # 拿着这个key 去上个接口里面得到想要的内容
    for key in keys:
        # 根据key值去上个接口里面提取内容
        # print(key)
        regex = r"'%s': '([\s\S]+?)'" % key
        # last_content是上个接口的内容 进行提取出来想要的内容
        match_obj = re.findall(regex, str(last_content))
        # 每次匹配出来内容都进行遍历装进list中
        for m in match_obj:
            present.append(m)
    # 从index 0开始  根据原值内容 直接进行替换，然后直接返回
    for i in range(0, len(present)):
        # key[i]是原来的值  present是获取的值 最后将特殊符号处理掉
        this_content = str(this_content).replace(keys[i], present[i]).replace('^', '')
    return this_content