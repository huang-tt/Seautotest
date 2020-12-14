# -*- coding: utf-8 -*-
#备注在jenkins里构建项目时，可能找不到项目地址，python项目的环境地址，以及第三库的环境地址，所以需要加入
import os,sys
dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir)
sys.path.append("F:\Python\Seautotest\\venv\Lib\site-packages")

from pathlib import Path

mali_dict = {'send_user': '741479651@qq.com',  # 发件人
             'password': 'qniasszasncebccj',  # 2密码
             'receive_users': '741479651@qq.com',  # 3收件人地址
             'receive_lisy': [],  # 4收件人list地址
             'subject': 'python自动化测试报告',  # 5主题
             'email_text': 'hi hello this report',  # 6邮件正文
             'server_address': 'smtp.exmail.qq.com',  # 7服务器地址
             'mail_type': 1}  # 8邮件类型
header = {
    '用例编号': 'id',
    '用例标题': 'title',
    '前置条件': 'condition',
    '测试功能点': 'testdot',
    '测试步骤': 'step',
    '操作': 'keyword',
    '页面': 'page',
    '元素': 'element',
    '测试数据': 'data',
    '预期结果': 'expected',
    '断言': 'assert',
    '设计者': 'designer',
    '步骤结果': 'score',
    '备注': 'remark',
}
report_header = {
    '用例编号': 'id',
    '用例标题': 'title',
    '测试功能点': 'testdot',
    '测试步骤': 'step',
    '操作': 'keyword',
    '页面': 'page',
    '元素': 'element',
    '测试数据': 'data',
    '输出数据': 'output',
    '预期结果': 'expected',
    '断言': 'assert',
    '设计者': 'designer',
    '步骤结果': 'score',
    '备注': 'remark',
}
header_custom = {'id': '用例编号', 'title': '用例标题', 'testdot': '测试功能点', 'step': '测试步骤',
                 'keyword': '操作', 'page': '页面', 'element': '元素', 'data': '测试数据', 'expected': '预期结果', 'assert': '断言',
                 'output': '输出数据',
                 'designer': '设计者', 'score': '步骤结果',
                 'remark': '备注'}

# case的文件的路径
file_case = str(Path('F:/Python/Seautotest/testcase') / ('test-case-yxy-api.xlsx'))
# element的文件的路径
file_element = str(Path('F:/Python/Seautotest/Element') / ('elements.xlsx'))
# junit测试报告的路径
file_junit = str(Path('F:/Python/Seautotest/Control/junit') / ('yxyapi' + '-' + 'junit' + '' + '.xml'))
# excel测试报告的路径
excel_report = str(Path('F:/Python/Seautotest/Control/report') / ('yxyapi-report.xlsx'))
# 生成xml的测试报告
file_xml = str(Path('F:/Python/Seautotest/Control/report') / ('yxyapi' + '-' + 'report' + '' + '.xlsx'))