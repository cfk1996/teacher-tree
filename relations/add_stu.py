# -*-coding: utf-8 -*-
'''老师增加学生模块
'''

import ast
import json

from handler import BaseHandler
from utils import get_db
from tornado_mysql import DatabaseError


class AddStuHandler(BaseHandler):
    '''老师添加学生
    处理/addTeacher请求
    '''
    async def get(self):
        year = self.get_argument('year')
        response = await self._get_info(year)
        self.finish(json.dumps(response, ensure_ascii=False))

    async def _get_info(self, year):
        conn = await get_db()
        try:
            cur = conn.cursor()
            sql = 'select user_id from identity where job={} and ' \
                  'date={}'
            await cur.execute(sql.format('学生', year))
            r = cur.fetchall()
            student = []
            for data in r:
                sql = 'select name, imgUrl from user where id={}'
                await cur.execute(sql.format(data[0]))
                r1 = cur.fetchone()
                student.append({'name': r1[0], 'imgUrl': r1[1], 'id': data[0]})
            response = {'data': student}
        except DatabaseError as e:
            print(e)
            response = {'status': 'database error'}
        finally:
            cur.close()
            conn.close()
        return response

    async def post(self):
        data = self.request.body.encode()
        data = ast.literal_eval(data)
        response = await self._add_stu(data)
        self.finish(json.dumps(response, ensure_ascii=False))

    async def _add_stu(self, data):
        tea_id = data['id']
        student = data['student']
        conn = await get_db()
        try:
            cur = conn.cursor()
            # 获取老师信息
            sql = 'select name, imgUrl from user where id={}'
            await cur.execute(sql.format(tea_id))
            r = cur.fetchone()
            for stu in student:
                sql = 'insert into relation(tea_id, stu_id, t_name, stu_name' \
                      ', t_imgurl) values ({}, {}, {}, {}, {})'
                await cur.execute(sql.format(tea_id, stu['id'], r[0],
                                             stu['name'], r[1]))
            response = {'status': '1'}
        except DatabaseError as e:
            print(e)
            response = {'status': 'database error'}
        finally:
            cur.close()
            conn.close()
        return response
