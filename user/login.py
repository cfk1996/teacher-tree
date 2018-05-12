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
    处理/login请求
    '''
    async def get(self):
        self.render('login.html')

    async def post(self):
        data = self.request.body.decode()
        data = ast.literal_eval(data)
        response = await self.authenticate(data)
        self.finish(json.dumps(response, ensure_ascii=False))

    async def authenticate(self, data):
        '''检验用户名与密码
        '''
        conn = await get_db()
        cur = conn.cursor()
        await cur.execute("select `password` from `user` where `name`=%s",
                          data['username'])
        r = cur.fetchone()
        cur.close()
        conn.close()
        password = md5(data['Password'])
        if not r:
            return {'status': 'user not exist'}
        if r[0] == password:
            return {'status': '1'}
        else:
            return {'status': 'wrong password'}
