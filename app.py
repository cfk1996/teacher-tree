# -*-coding: utf-8 -*-
'''application定义模块
'''

import os
import tornado.web

from user.login import LoginHandler
from test import TextHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # (r"/", IndexHandler),
            (r"/login", LoginHandler),
            (r"/text", TextHandler),
            # (r"/register", RegisterHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            cookie_secrete="",
            login_url="/login",
            debug=True,
        )
        super(Application, self).__init__(handlers, **settings)
