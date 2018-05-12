# -*-coding: utf-8 -*-
'''以学生身份为中心的师承树
'''

import json

from handler import BaseHandler
from utils import get_db
from tornado_mysql import DatabaseError


class StuTreeHandler(BaseHandler):
    '''以学生身份为中心的师承树
    处理/relationTree?id=xxx请求
    '''
    async def get(self):
        id = self.get_argument('id')
        response = await self._get_info(id)
        self.finish(json.dumps(response, ensure_ascii=False))

    async def _get_info(self, id):
        conn = await get_db()
        try:
            response = {}
            cur = conn.cursor()
            # 获取个人信息
            sql = 'select date from identity where user_id={} and ' \
                  'job={}'
            await cur.execute(sql.format(id, '学生'))
            r0 = cur.fetcheone()
            date = r0[0]
            # 获取老师信息
            sql = 'select tea_id, t_name from relation where ' \
                  'stu_id={}'
            await cur.execute(sql.format(id))
            r1 = cur.fetchall()
            response['data'] = []
            # 获取同学信息
            for data in r1:
                sql = 'select stu_id, stu_name from relation where ' \
                      'tea_id={}'
                await cur.execute(sql.format(data[0]))
                r2 = cur.fetchall()
                older, peers, younger = [], [], []
                for m in r2:
                    sql = 'select date from identity where user_id={} and ' \
                          'job={}'
                    await cur.execute(sql.format(m[0], '学生'))
                    r3 = cur.fetcheone()
                    if r3[0] > date:
                        younger.append({'id': m[0], 'name': m[1]})
                    elif r3[0] == date:
                        peers.append({'id': m[0], 'name': m[1]})
                    else:
                        older.append({'id': m[0], 'name': m[1]})
                response['data'].append({'techerId': data[0],
                                         'teacherName': data[1],
                                         'older': older, 'peers': peers,
                                         'younger': younger})
        except DatabaseError as e:
            print(e)
            response = {'status': 'database error'}
        finally:
            cur.close()
            conn.close()
        return response
