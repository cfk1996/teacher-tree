# -*-coding: utf-8 -*-
'''以老师的身份获取师承树关系
'''

import json

from handler import BaseHandler
from utils import get_db
from tornado_mysql import DatabaseError


class ＴeachTreeHandler(BaseHandler):
    '''以老师为核心获取师承树关系
    处理/relationTeacherTree?id=xxx请求
    '''
    async def get(self):
        id = self.get_argument('id')
        response = await self._get_info(id)
        self.finish(json.dumps(response, ensure_ascii=False))

    async def _get_info(self, id):
        conn = await get_db()
        try:
            cur = conn.cursor()
            sql = 'select stu_id from relation where ted_id={}'
            await cur.execute(sql.format(id))
            r = cur.fetchall()
            response = {}
            for data in r:
                sql = 'select user.name, identity.date from user join ' \
                      'identity on user.id=identity.user_id where ' \
                      'user_id={} and job={}'
                await cur.execute(sql.format(data[0], '学生'))
                r1 = cur.fetchall()
                for m in r1:
                    if m[1] not in response:
                        response[m[0]] = [{'id': data[0], 'name': m[0]}]
                    else:
                        response[m[0]].append({'id': data[0], 'name': m[0]})
        except DatabaseError as e:
            print(e)
            response = {'status': 'database error'}
        finally:
            cur.close()
            conn.close()
        return response
