import random
# from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
# from Crypto.PublicKey import RSA
import base64
from pathlib import Path


import configparser
# from control.projectpath import utilsconf_dir
"""
自定义函数，生成相对于的加密串，手机号等信息
"""

pub = '\n'.join([
    '-----BEGIN PUBLIC KEY-----',
    '',
    '-----END PUBLIC KEY-----'
])
path = str(Path('control/book') / ('txt_final.txt'))


def create_phone():
    # 第二位数字
    second = [3, 4, 5, 7, 8][random.randint(0, 4)]

    # 第三位数字
    third = {
        3: random.randint(0, 9),
        4: [5, 7, 9][random.randint(0, 2)],
        5: [i for i in range(10) if i != 4][random.randint(0, 8)],
        7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
        8: random.randint(0, 9),
    }[second]

    # 最后八位数字
    suffix = random.randint(9999999, 100000000)
    phone = "1{}{}{}".format(second, third, suffix)

    writetxt(phone)
    # 拼接手机号
    return phone


# 加密的方法
def setrsa(tw):
    # public_key = RSA.importKey(pub)
    # input = encrypt(public_key, bytes(str(tw), encoding='utf-8'))
    return tw
#
#
# def encrypt(pub, message):
#     cipher = Cipher_pkcs1_v1_5.new(pub)
#     cipher_text = base64.b64encode(cipher.encrypt(message))
#     return str(cipher_text)

    # 用例表


# 方法可以写入token和普通常量
def writetxt(phone):
    print(phone)
    f = open(path, 'a')
    f.write(phone + '\n')
    f.close()


def gettxt():
    try:
        f = open(path, 'r')
        sourceInLines = f.readlines()  # 按行读出文件内容
        f.close()
        return sourceInLines[0]
    except:
        return 'test'


# 获取最新的验证码链接数据库获取

def getcode(t=str(gettxt())):
    import pymysql
    # 测试
    conn = pymysql.connect(
        host="",
        port='',
        user='',
        password='',
        database='',
        charset=''

    )
    try:
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        sql = 'SELECT * FROM sms WHERE mobile=%s ORDER BY create_time DESC LIMIT 1;' % t
        cursor.execute(sql)
        results = cursor.fetchall()
        phone = results[0]['dynamic_code']
        # 记录当前手机号方便复用 存入csv文件内
        return phone
    except:
        # logger.error('error:Verification code not found')
        return ''


def gettoken():
    f = open(path, 'r')
    sourceInLines = f.readlines()  # 按行读出文件内容
    try:
        return sourceInLines[1]
    except:
        print('no found token')
    f.close()


def get_configInfo(section, option):
    conf = configparser.ConfigParser()
    conf.read(utilsconf_dir, encoding='utf-8')
    value = conf.get(section, option)
    return value



