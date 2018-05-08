# -*-coding: utf-8 -*-
'''师承树
'''

import tornado.ioloop
import tornado.httpserver
from app import Application

PORT = 10000


def main():
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(PORT)
    print('start listening on port {}'.format(PORT))
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
