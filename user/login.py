# -*-coding: utf-8 -*-
'''用户登录模块
处理/login请求
GET: 返回登录页面
POST: 验证账户
'''

import ast
import json

from handler import BaseHandler
from utils import md5, get_db


class LoginHandler(BaseHandler):
    '''登录请求handler
    '''
    async def get(self):
        self.render('login.html')

    async def post(self):
        data = self.request.body.decode()
        data = ast.literal_eval(data)
        response = await self.authenticate(data)
        if response['result'] is True:
            self.render('/')
        else:
            self.finish(json.dumps(response, ensure_ascii=False))

    async def authenticate(self, data):
        '''检验用户名与密码
        '''
        conn = await get_db()
        cur = conn.cursor()
        await cur.execute("select `password` from `user` where `name`=%s",
                          data['name'])
        r = cur.fetchone()
        cur.close()
        conn.close()
        password = md5(data['pass'])
        if not r:
            return {'result': 'user not exist'}
        if r[0] == password:
            return {'result': True}
        else:
            return {'result': 'wrong password'}
