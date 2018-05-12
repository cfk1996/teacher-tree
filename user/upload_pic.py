# -*-coding: utf-8 -*-
'''上传图片模块
图片为用户头像
'''

import ast
import json

from utils import get_db
from handler import BaseHandler
from tornado_mysql import DatabaseError


class UploadPicHandler(BaseHandler):
    '''上传图片模块
    处理/upload?id=xxx请求，将图片保存至服务器，并返回图片地址
    '''
    def post(self):
        id = self.get_argument('id')
        pass