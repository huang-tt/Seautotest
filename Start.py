# -*- coding: UTF-8 -*-
#备注在jenkins里构建项目时，可能找不到项目地址，python项目的环境地址，以及第三库的环境地址，所以需要加入
import os,sys
dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir)
sys.path.append("F:\Python\Seautotest\\venv\Lib\site-packages")

from Control.Autotest import Autotest
import sys
from datetime import datetime
import os

start_se_time = datetime.now()
# 将工程根目录加入到python搜索路径中
sys.path.append('..')
# 兼容后期格式，是接口自动化还是web自动化app自动化，数据库，小程序 h5等自动化测试，以接口为主
desired_caps = {'genre': 'api'}
print(desired_caps)
autotest = Autotest(desired_caps)
# 执行测试
autotest.play()
# dd报警
autotest.alarm()
# 生成allure测试报告
# 参考资料 生成xml报告形式：https://llg.cubic.org/docs/junit/
try:
    os.system('allure serve F:/Python/Seautotest/Control/junit')
except BaseException:
    print("allure测试报告,生成错误")
# 发送测试报告到邮箱

end_se_time = datetime.now()

print(end_se_time - start_se_time)