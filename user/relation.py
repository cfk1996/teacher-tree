# -*-coding: utf-8 -*-
'''添加师生关系模块
'''

import json
import ast

from handler import BaseHandler
from utils import get_db
from tornado_mysql import DatabaseError


class RelationHandler(BaseHandler):
    '''添加师生关系
    处理/teachers请求
    '''
    async def post(self):
        data = self.request.body.encode()
        data = ast.literal_eval(data)
        response = await self._add_info(data)
        self.finish(json.dumps(response, ensure_ascii=False))

    async def _add_info(self, data):
        conn = await get_db()
        try:
            cur = conn.cursor()
            for tech in data['teacher']:
                await cur.execute('insert into relation(tea_id, stu_id)'
                                  'values ({}, {})'.format(tech, data['id']))
            response = {'status': 'success'}
        except DatabaseError as e:
            print(e)
            response = {'status': 'database error'}
        finally:
            cur.close()
            conn.close()
        return response
