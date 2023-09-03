import tornado
from .base import BaseHandler


class ErrorHandler(tornado.web.ErrorHandler, BaseHandler):
    pass
