# -*-coding: utf-8 -*-
'''application定义模块
'''

import os
import tornado.web

from test import TextHandler
from user.add_identity import AddIdentityHandler
from user.add_info import AddInfoHandler
from user.infomation import InfoHandler
from user.login import LoginHandler
from user.register import RegisterHandler
from user.relation import RelationHandler
from user.upload_pic import UploadPicHandler
from user.user_info import UserInfoHandler
from relations.stu_tree import StuTreeHandler
from relations.teach_tree import TeachTreeHandler


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            # (r"/", IndexHandler),
            (r"/identity", AddIdentityHandler),
            (r"/login", LoginHandler),
            (r"/text", TextHandler),
            (r"/myinfo", AddInfoHandler),
            (r"/infomation", InfoHandler),
            (r"/login", LoginHandler),
            (r"/newUser", RegisterHandler),
            (r"/teachers", RelationHandler),
            (r"/upload", UploadPicHandler),
            (r"/settings", UserInfoHandler),
            (r"/relationTree", StuTreeHandler),
            (r"realtionTeacherTree", TeachTreeHandler)
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
