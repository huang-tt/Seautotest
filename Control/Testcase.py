# -*- coding: UTF-8 -*-
"""
1.执行用例
2.分辨是接口自动化还是ui数据等
3.记录测试结果和输出测试报告
"""

#备注在jenkins里构建项目时，可能找不到项目地址，python项目的环境地址，以及第三库的环境地址，所以需要加入
import os,sys
dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir)
sys.path.append("F:\Python\Seautotest\\venv\Lib\site-packages")

from Control.Log import logger
from Control.Data import replace, acquire
from Control import Httpcaps
import threading
import time


class TestCase:
    _instance_lock = threading.Lock()

    def __init__(self, junit):
        self.junit = junit

        # 记录多少用例没有通过
        self.step_fail = 0
        # 记录出错的用例
        self.step_error = 0
        # 出错用例的功能点
        self.errors_detail = ''

        # 上个步骤
        self.last_step = {}

    # 采用单例的设计模式  可能没什么实际效果~~
    def __new__(cls, *args, **kwargs):
        if not hasattr(TestCase, "_instance"):
            with TestCase._instance_lock:
                if not hasattr(TestCase, "_instance"):
                    TestCase._instance = object.__new__(cls)
        return TestCase._instance

    #  执行测试用例
    def run(self, case):
        # 当前执行的用例
        self.case = case
        # 记录执行的用例结果，新的用例来了，就清空了
        steps = []
        for index, step in enumerate(self.case['steps']):
            if self.last_step:
                # 从上个接口提取到下个接口想要的数据
                step['data'] = acquire(str(self.last_step['output']), str(step['data']), self.case)
                # 查看上个测试数据里面有没有这个内容
                # 如果里面有#号，则吧测试数据重组
                # 将测试数据进行重组，调用自定义函数 计算出结果
            if step['data']:
                step['data'] = replace(str(step['data']))
                # step['data'] = replace(str(step))
            if '#' in str(step['data']):
                # 只切割最后一个#
                data_list = str(step['data']).rsplit('#', 1)
                step['data'] = data_list[0]
                sleep_time = data_list[1].split('=')
                logger.info('{}'.format(sleep_time))
                time.sleep(float(sleep_time[1]))
            self.last_step = getattr(Httpcaps, 'http_requests')(step, self.junit)
            if self.last_step['score'] != 'Pass':
                self.step_fail += 1
            steps.append(self.last_step)
            # print("===============self.case['steps']的值",self.case[steps])

            # try:
               # 上一个步骤不为空，则进行判断是否需要接口关联

            # except Exception as excepetion:
            #     # 将此用例等于不通过
            #     step['score'] = 'Fail'
            #     step['_resultinfo'] = 'exception：%s' % excepetion
            #     self.step_error += 1
            #     logger.info(step)
            #     self.junit.failure(
            #         'testdot:' + step['testdot'] + ' - ' + 'step:' + step['no'] + ' - ' + 'element:' + step[
            #             '_element'] + ' - ' + 'error:%s' % excepetion)
            #     self.errors_detail += step['testdot'] + '--' + '{}'.format(excepetion)
            #     steps.append(step)
            #     logger.error('error:interface and element not found%s' % excepetion)
            #     logger.error('error:%s' % excepetion)
            #     logger.info('上一条用例：' + str(self.last_step))
                # 记录生成的测试结果，生成测试报告excel版本
            self.case['steps'] = steps
        return self.case


"""
 第一个需求：接口数据和上一步骤进行关联
 1.先拿到执行的上一个步骤
 2.拿到步骤之后，去取里面的值
 3.正则提取出来想要的内容
 4.将想要的内容拼接到下个接口里面
 5.使用发送请求并记录结果                 ok

 第二个需求：接口报警发送到钉钉群里
 1.接口不通过发送信息到钉钉
 2.有当前用例的标题和步骤编号
 3.以及不通过的原因和接口返回的数据
 第三个需求：定时监控或者实时监控
 1.jenkins方案设置固定时间执行脚本
 2.Jenkins实时执行自动化脚本项目
 3.调度执行脚本，设置固定时间监控等
 第四个需求：兼容多个base_url
 其他需求：
  1.关于添加菜单
    (1):使用ui自动化添加菜单
    (2):使用接口添加菜单
    (3):数据格式采用json进行添加，一劳永逸。
"""