# -*-coding: utf-8 -*-
'''获取用户全部信息模块
'''
import json

from handler import BaseHandler
from utils import get_db
from tornado_mysql import DatabaseError


class UserInfoHandler(BaseHandler):
    '''获取用户全部信息
    处理/settings请求
    '''
    async def get(self):
        id = self.get_argument('id')
        response = await self._get_info(id)
        self.finish(json.dumps(response, ensure_ascii=False))

    async def _get_info(self, id):
        conn = await get_db()
        try:
            cur = conn.cursor()
            sql = 'select name, sex, email, city, imgUrl from user' \
                  'where id={}'
            await cur.execute(sql.format(id))
            r1 = cur.fetchone()

            await cur.execute('select job, date from identity where'
                              'user_id={}'.format(id))
            r2 = cur.fetchall()
            job_list = []
            for data in r2:
                job_list.append({'identity': data[0], 'date': data[1]})

            await cur.execute('select tea_id, t_name, t_imgurl from'
                              'relation where stu_id={}'.format(id))
            r3 = cur.fetchall()
            teacher_list = []
            for data in r3:
                teacher_list.append({'id': data[0], 'name': data[1],
                                     'imgUrl': data[2]})
            response = {'name': r1[0], 'sex': r1[1], 'email': r1[2],
                        'city': r1[3], 'job': job_list,
                        'teacherList': teacher_list}
        except DatabaseError as e:
            print(e)
            response = {'status': 'database error'}
        finally:
            cur.close()
            conn.close()
        return response
