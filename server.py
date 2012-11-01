#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import uuid
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import pika
from pika.adapters import TornadoConnection
from tornado.options import define, options
from consumer import PikaClient
import logging

LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) -35s %(lineno) -5d: %(message)s')

define("port", default=8888, help="run on the given port", type=int)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class WSHandler(tornado.websocket.WebSocketHandler):

    waiters = set()

    def allow_draft76(self):
        # for iOS 5.0 Safari
        return True

    def open(self):
        self.application.pc.add_event_listener(self)
        WSHandler.waiters.add(self)
        logging.info("WebSocket %s opened", len(WSHandler.waiters))

    def on_close(self):
        logging.info("WebSocket %s closed", len(WSHandler.waiters))
        self.application.pc.remove_event_listener(self)
        WSHandler.waiters.remove(self)

    def on_message(self, message):
        logging.info("got message %r", message)

        WSHandler.send_updates(message)

    @classmethod
    def send_updates(cls, message):
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(message)
            except:
                logging.error("Error sending message", exc_info=True)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r'/socket.io', WSHandler)
        ]
        settings = dict(
            cookie_secret="__TODO__:__GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            xsrf_cookies=True,
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

    application = Application()
    io_loop = tornado.ioloop.IOLoop.instance()

    pc = PikaClient('amqp://guest:guest@localhost:5672/%2F', io_loop)
    application.pc = pc
    application.pc.connect()

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)

    io_loop.start()
