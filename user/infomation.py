# -*-coding: utf-8 -*-
'''查询基础信息模块
'''

import json

from handler import BaseHandler
from utils import get_db
from tornado_mysql import DatabaseError


class InfoHandler(BaseHandler):
    '''查询基础信息模块:Ａ查询Ｂ的信息
    处理/infomation?name=xxx请求
    '''
    async def get(self):
        name = self.get_argument('name')
        response = await self._get_info(name)
        self.finish(json.dumps(response, ensure_ascii=False))

    async def _get_info(self, name):
        conn = await get_db()
        try:
            cur = conn.cursor()
            sql = 'select name, sex, email, city, imgUrl, id from user ' \
                  'where name={}'
            await cur.execute(sql.format(name))
            r = cur.fetcheall()
            response = {'data': []}
            for m in r:
                response['data'].append({'name': m[0], 'sex': m[1],
                                         'email': m[2], 'city': m[3],
                                         'imgUrl': m[4], 'id': m[5]})
        except DatabaseError as e:
            print(e)
            response = {'status': 'database error'}
        finally:
            cur.close()
            conn.close()
        return response
