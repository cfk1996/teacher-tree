# -*-coding: utf-8 -*-
'''完善用户职业信息
'''

import json
import ast

from utils import get_db
from handler import BaseHandler
from tornado_mysql import DatabaseError


class AddIdentityHandler(BaseHandler):
    '''完善个人职业信息
    处理/identity请求
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
            await cur.execute('delete from identity where id={}'.format(
                data['id']))
            for job in data['job']:
                await cur.execute('insert into identity(user_id, job, date)'
                                  'value ({}, {}, {})'.format(data['id'],
                                                              job['identity'],
                                                              job['date']))
            response = {'status': '1'}
        except DatabaseError as e:
            print(e)
            response = {'status': 'database error'}
        finally:
            cur.close()
            conn.close()
        return response
