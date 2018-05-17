# -*-coding: utf-8 -*-
'''上传图片模块
图片为用户头像
'''

import json

from utils import get_db
from handler import BaseHandler
from tornado_mysql import DatabaseError


class UploadPicHandler(BaseHandler):
    '''上传图片模块
    处理/upload?id=xxx请求，将图片保存至服务器，并返回图片地址
    '''
    async def post(self):
        id = self.get_argument('id')
        file = self.request.files['file']
        file_path = id + '.jpg'
        for pic in file:
            with open(file_path, 'wb') as f:
                f.write(pic['body'])
        conn = await get_db()
        try:
            cur = conn.cursor()
            sql = 'insert into user(imgUrl) values ({}) where id={}'
            await cur.execute(sql.format(file_path, id))
        except DatabaseError as e:
            print(e)
        finally:
            cur.close()
            conn.close()
        self.finish(json.dumps({'newPath': file_path}, ensure_ascii=False))
