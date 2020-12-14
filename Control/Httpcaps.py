#备注在jenkins里构建项目时，可能找不到项目地址，python项目的环境地址，以及第三库的环境地址，所以需要加入
import os,sys
dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir)
sys.path.append("F:\Python\Seautotest\\venv\Lib\site-packages")

import requests
from Control.Log import logger
from Control.Data import *
import base64
from Control.Data import element_tojson
import ast  #可以将字符串转为字典


def http_requests(step, junit):
    # 获取到配置的头部文件数据
    element = file_element
    # 读取链接和元素表格全部内容
    excel_element = Excel('r', element)
    # 元素和接口转换为json，切片是为了去除表格的第一行
    e = excel_element.read()[2:3]
    elements = element_tojson(e)

    logger.info('当前执行的步骤')
    logger.info(step)
    # 获取当前的请求类型
    sort = step['element']['type']
    # print("---------当前请求类型sort等于",sort)
    # 获得当前的url
    url = step['element']['url']
    # print("---------当前请求url等于", url)
    data = datatating(step['data'])
    # print("---------当前请求data等于", data)
    # 发送请求之前判断一下用例里面有没有headers,有则进行使用没有则使用element的默认headers
    logger.info(data.get('headers'))
    if data.get('headers') is not None:
        headers = data.get('headers', {})
    # 是空 则去读取element里面的
    else:
        # print("============请求头是：",elements)
        headers = elements['baseurl']['headers']
        # print("===============请求头",headers,type(headers))

    if sort == 'post':
        d = eval(str(data))
        # print("==========d的值：",d)
        #base64模块提供将一种二进制转化为另一种二进制的方法，后者可全部由64个字符表示
        # fileorbase64 = d.get('swt', '')
        # print("============ fileorbase64的值：",fileorbase64)
        # if fileorbase64 == 'file':
        #     del d['swt']
        #     d['FILES'] = open('F:/Python/Seautotest/Control/file/' + str(d.get('FILES')), 'rb').read()
        # elif fileorbase64 == 'base64':
        #     del d['swt']
        #     d['FILES'] = str(base64.b64encode(open('F:/Python/Seautotest/Control/file/' + str(d.get('FILES')), 'rb').read())) + '.jpg'
        # data['files'] = d
        #发起requests.post请求
        r = requests.post(url, json=data,headers=ast.literal_eval(headers))
        # print("---------------r的值是：",r)
        # print("================r.json()的值",r.json())
    elif sort == 'get':
        #发起requests.get请求
        # 当下载大的文件的时候，建议使用stream,默认情况下是false，他会立即开始下载文件并存放到内存当中，倘若文件过大就会导致内存不足的情况
        r = requests.get(url, data,headers=ast.literal_eval(headers),stream=True)
    # 记录为何不通过
    content = ''
    # 记录是否通过
    list_record = []

    status = r.status_code
    # logger.info(status)
    # 1.接口不等于200，不进行验证和断言
    if status != 200:
        step['score'] = 'Fail'
        logger.info(status)
        logger.info(r.url)
        logger.error('接口出错了{}接口的url为:{}'.format(status, r.url))
        return step
    # 如果是登录的接口，将登录的token写入文本

    # if testdot in ('登录接口验证'):
    #     writetoken(response['data']['token'])

    # 2.验证断言内容 断言只有在预期结果写了#('xxx','xxx')这种才会进行课程
    #strip（）介绍：删除开头或是结尾的字符。
    if str(step['assert']).strip():
        print("=======step['assert']的值",step['assert'],type(step['assert']))
        # 1预期结果 2需要断言的内容 是元祖类型 ,返回：断言通过 返回'' ，反之返回不通过的字段
        is_as_pass = asset_content( step['assert'],r.json())
        # 通过
        if is_as_pass == '':
            content += '断言通过'
        # 不通过
        else:
            list_record.append(1)
            content += '断言不通过%s' % is_as_pass
    # 3.验证返回值json格式
    if str(step['expected']).strip():
        response, expected = rplaceto_tf(r.json(), step['expected'])
        result = iscompare_json(expected, response)
        if result == 'Pass':
            content += '对比格式通过'
        else:
            list_record.append(1)
            content += 'json对比格式不通过'

    if len(list_record) >= 1:
        step['score'] = 'Fail'
        junit.failure('testdot:' + step['testdot'] + '-' + 'step:' + step['no'] + '-' + 'element:' + step[
            '_element'] + '-' + ', %s' % content)
    else:
        step['score'] = 'Pass'
    step['_resultinfo'] = content
    step['resultinfo'] = content
    step['output'] = r.json()
    logger.info('下面是返回值' + step['testdot'])
    logger.info(r.json())
    return step

