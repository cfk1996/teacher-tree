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
            sql = 'select name from user where id={}'
            await cur.execute(sql.format(data['id']))
            r = cur.fetchone()
            stu_name = r[0]
            for tech in data['teacher']:
                sql = 'select imgUrl from user where id={}'
                await cur.execute(sql.format(tech['id']))
                r = cur.fetchone()
                sql = 'insert into relation(tea_id, t_name, stu_id,' \
                      't_imgurl, stu_name) values ({}, {}, {}, {}, {})'
                await cur.execute(sql.format(tech['id'], tech['name'],
                                             data['id'], r[0] or ' ',
                                             stu_name))
            response = {'status': '1'}
        except DatabaseError as e:
            print(e)
            response = {'status': 'database error'}
        finally:
            cur.close()
            conn.close()
        return response
