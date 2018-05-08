# -*-coding: utf-8 -*-
'''注册模块
'''

import json
import ast

from handler import BaseHandler
from utils import get_db, md5
from tornado_mysql import DatabaseError


class RegisterHandler(BaseHandler):
    '''处理/register请求
    GET: 返回注册页面
    POST: 注册账户
    '''
    def get(self):
        self.render('register.html')

    async def post(self):
        data = self.request.body.encode()
        data = ast.literal_eval(data)
        response = await self.register(data)
        self.finish(json.dumps(response, ensure_ascii=False))

    async def register(self, data):
        password = md5(data['pass'])
        conn = await get_db()
        cur = conn.cursor()
        try:
            await cur.execute("insert into `user`(phone, password) values ({}, \
                               {})".format(data['phone'], password))
            response = {'info': 'success'}
        except DatabaseError as e:
            response = {'info': 'Name already exists!'}
            print(e)
        finally:
            cur.close()
            conn.close()
        return response
