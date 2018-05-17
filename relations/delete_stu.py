# -*-coding: utf-8 -*-
'''老师删除学生模块
'''

import ast
import json

from handler import BaseHandler
from utils import get_db
from tornado_mysql import DatabaseError


class DeleteStuHandler(BaseHandler):
    '''老师删除学生模块
    处理deleteStudentList请求
    '''
    async def get(self):
        id = self.get_argument('Id')
        year = self.get_argument('year')
        response = await self._get_info(id, year)
        self.finish(json.dumps(response, ensure_ascii=False))

    async def _get_info(self, id, year):
        conn = await get_db()
        try:
            cur = conn.cursor()
            sql = 'select stu_id from relation where tea_id={}'
            await cur.execute(sql.format(id))
            r = cur.fetchall()
            stu_lists = []
            # 符合要求的学生id列表
            for data in r:
                sql = 'select date from identity where user_id={}' \
                      'and job={}'
                await cur.execute(sql.format(data[0], '学生'))
                r1 = cur.fetchone()
                if r1[0] == year:
                    stu_lists.append(data[0])
            stu_info = []
            for _id in stu_lists:
                sql = 'select name, imgUrl from user where id={}'
                await cur.execute(sql.format(_id))
                r2 = cur.fetchone()
                stu_info.append({'name': r2[0], 'imgUrl': r2[1], 'id': _id})
            response = {'data': stu_info}
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
        response = await self._delete(data)
        self.finish(json.dumps(response, ensure_ascii=False))

    async def _delete(self, data):
        tea_id = data['id']
        student = data['student']
        conn = await get_db()
        try:
            cur = conn.cursor()
            for stu in student:
                sql = 'delete from relation where tea_id={} and ' \
                      'stu_id={}'
                await cur.execute(sql.format(tea_id, stu['id']))
            response = {'status': '1'}
        except DatabaseError as e:
            print(e)
            response = {'status': 'database error'}
        finally:
            cur.close()
            conn.close()
        return response
