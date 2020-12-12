# -*- coding: UTF-8 -*-
import logging
import datetime
from pathlib import Path
import sys
def mkdir(p):
    path = Path('F:/Python/Seautotest/Control/' + p)
    # 如果文件不存在 则创建
    if not path.is_dir():
        path.mkdir()

def today():
    #获取当前时间
    now = datetime.datetime.now()
    #返回时间格式为年月日时分秒
    return now.strftime('%Y-%m-%d')


# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger("Seautotest")

# 指定logger输出格式
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(filename)s line:%(lineno)d: %(message)s')

mkdir('log')
# 文件日志
log_file = str(Path('F:/Python/Seautotest/Control/log') / '{}.log'.format(today()))
file_handler=logging.FileHandler(log_file, mode='a', encoding='utf-8', delay=False)
# file_handler = logging.FileHandler(filename=log_file, encoding="utf-8")
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 指定日志的最低输出级别，默认为WARN级别
# DEBUG，INFO，WARNING，ERROR，CRITICAL
logger.setLevel(logging.INFO)