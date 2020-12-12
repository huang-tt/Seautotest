#python读取，写入和更新xml文件
#XML 指可扩展标记语言（eXtensible Markup Language）， 被设计用来传输和存储数据。python中有三个模块解析xml文件：DOM， ElementTree，SAX
#DOM将XML数据在内存中解析成一个树，通过对树的操作来操作XML。python的xml.dom.minimom模块实现了DOM
import timeit
from xml.dom.minidom import Document
from pathlib import Path
from Control.Data import gettime
from datetime import datetime
from Control.Log import logger

#DOM写入xml文件主要是创建dom树，然后创建根结点，创建子节点并加入到根节点，最后将整个dom树写入文件
class Junit:
    def __init__(self):
        # 创建DOM文档对象,创建树
        self.doc = Document()
        # 程序开始时间
        self.pstarttime =  datetime.now()
        # 创建用例套件集，创建名为'testsuites'的节点
        self.testsuites = self.doc.createElement('testsuites')
        #将self.testsuites设为self.doc的子节点
        self.doc.appendChild(self.testsuites)
        # 当前时间
        self.nowtime = gettime()
        # 创建用例套件
        self.testsuite = self.doc.createElement('testsuite')

    # 测试用例套件
    #setAttribute() 方法创建或改变某个新属性。
    #如果指定属性已经存在,则只设置该值。
    def suite(self, error, failures, tests, skips):
        # 错误用例的数量
        self.testsuite.setAttribute('errors', str(error))
        # 失败用例的数量
        self.testsuite.setAttribute('failures', str(failures))
        # 项目的名称
        self.testsuite.setAttribute('hostname', 'seautotest')
        # 用例数量
        self.testsuite.setAttribute('tests', str(tests))
        # 跳过用例的数量
        self.testsuite.setAttribute('skipped', str(skips))
        # 项目类型
        self.testsuite.setAttribute('name', 'API')
        # 时间
        self.testsuite.setAttribute('timestamp', str(datetime.isoformat(self.pstarttime)))

        self.settime()

    # 每条用例是一个case
    def case(self, id, title, time):
        # 创建case标签
        self.testcase = self.doc.createElement('testcase')
        # 用例的名称
        self.testcase.setAttribute('name', str(title))
        self.case_timer = time
        self.settime()
    # 跳过用例的case
    def skip_case(self, message):
        skip = self.doc.createElement('skipped')
        skip.setAttribute('message', message)
        self.testcase.appendChild(skip)

    # 设置时间
    def settime(self):
        # logger.info(self.time)
        endtime = datetime.now()
        # 单个用例的执行时间
        td = endtime - self.case_timer
        time = float(
            (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6)) / 10 ** 6
        self.testcase.setAttribute('time', str(time))
        self.testcase.setAttribute('priority', 'M')
        self.testsuite.appendChild(self.testcase)

    # 失败的用例
    def failure(self, message):
        # 创建失败用例的标签
        failure = self.doc.createElement('failure')
        # 为什么失败了这个用例
        failure.setAttribute('message', str(message))
        # 类型为失败
        failure.setAttribute('type', 'Failure')
        # 添加到testcase下
        self.testcase.appendChild(failure)

    # 生成xml  是allure的数据源
    def write_toxml(self):
        # 计算执行的时间， 用当前时间-开始时间 是总耗时
        td = datetime.now() - self.pstarttime
        td_time = float(
            (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10 ** 6)) / 10 ** 6
        self.testsuite.setAttribute('time', '%s' % td_time)
        self.testsuites.appendChild(self.testsuite)
        file = Path('F:/Python/Seautotest/Control/junit') / ('API' + '-' + 'ReportJunit@' + self.nowtime + '.xml')
        f = open(file, 'w')
        self.doc.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='gbk')
        f.close()