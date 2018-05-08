# -*-coding: utf-8 -*-

from handler import BaseHandler
from utils import get_db
from tornado_mysql import DatabaseError


class TextHandler(BaseHandler):
    async def get(self):
        conn = await get_db()
        cur = conn.cursor()
        try:
            print(1111)
            await cur.execute("select id, name, password from user")
            print(2222)
            r = cur.fetchone()
            for m in r:
                print('{} . type={}'.format(m, type(m)))
        except DatabaseError as e:
            response = {'info': 'Name already exists.'}
            print(e)
        finally:
            cur.close()
            conn.close()
        self.finish()

