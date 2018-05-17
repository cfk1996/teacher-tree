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
            # 个人信息
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
            # 已建立的老师关系
            await cur.execute('select tea_id, t_name, t_imgurl from'
                              'relation where stu_id={}'.format(id))
            r3 = cur.fetchall()
            pickTeachers = []
            for data in r3:
                pickTeachers.append({'id': data[0], 'name': data[1],
                                     'imgUrl': data[2]})
            # 所有老师
            teacherList = []
            sql = 'select user_id from identity where job={}'
            await cur.execute(sql.format('教师'))
            r4 = cur.fetchall()
            for data in r4:
                sql = 'select name, imgUrl from user where id={}'
                await cur.execute(sql.format(data[0]))
                r5 = cur.fetchone()
                teacherList.append({'id': data[0], 'name': r5[0],
                                    'imgUrl': r5[1]})
            response = {'name': r1[0], 'sex': r1[1], 'email': r1[2],
                        'city': r1[3], 'job': job_list,
                        'teacherList': teacherList,
                        'pickTeachers': pickTeachers}
        except DatabaseError as e:
            print(e)
            response = {'status': 'database error'}
        finally:
            cur.close()
            conn.close()
        return response
