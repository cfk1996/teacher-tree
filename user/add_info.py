# -*-coding: utf-8 -*-
'''完善用户基础信息模块
用户注册后，完善信息
'''

import ast
import json

from utils import get_db
from handler import BaseHandler
from tornado_mysql import DatabaseError


class AddInfoHandler(BaseHandler):
    '''完善个人基础信息
    处理/myinfo请求
    '''
    async def get(self):
        phone = self.get_argument('phone')
        response = await self.get_info(phone)
        self.finish(json.dumps(response, ensure_ascii=False))

    async def get_info(self, phone):
        conn = await get_db()
        try:
            cur = conn.cursor()
            await cur.execute('select id, name, age, study_school,'
                              'school_day, identity, work_school, link'
                              'from user'
                              'where phone={}'.format(phone))
            r = cur.fetchone()
            response = {'id': r[0], 'name': r[1], 'age': r[2],
                        'study_school': r[3], 'school_day': r[4],
                        'identity': r[5], 'work_school': r[6],
                        'link': r[7]}
        except DatabaseError as e:
            print(e)
            response = {'info': 'database error'}
        finally:
            cur.close()
            conn.close()
        return response

    async def post(self):
        data = self.request.body.encode()
        data = ast.literal_eval(data)
        response = await self.add_info(data)
        self.finish(json.dumps(response, ensure_ascii=False))

    async def add_info(self, data):
        conn = await get_db()
        try:
            cur = conn.cursor()
            await cur.execute('update user set name={}, sex={}, email={},'
                              'city={}, id={}'.format(data['name'],
                                                      data['sex'],
                                                      data['email'],
                                                      data['city'],
                                                      int(data['id'])))
            response = {'status': 'success'}
        except DatabaseError as e:
            print(e)
            response = {'status': 'database error'}
        finally:
            cur.close()
            conn.close()
        return response
