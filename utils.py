# -*-coding: utf-8 -*-
'''工具模块
'''
import tornado_mysql
import hashlib


# 返回数据库连接
async def get_db():
    conn = await tornado_mysql.connect(host='127.0.0.1', port=3306,
                                       user='root', password='123456',
                                       db='tree')
    return conn


# md5加密
def md5(string):
    md5 = hashlib.md5()
    md5.update(string.encode())
    return md5.hexdigest()