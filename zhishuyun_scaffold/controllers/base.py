from loguru import logger
from uuid import uuid4
from zhishuyun_scaffold.settings import HTTP_HOST, HTTP_PORT
from rest_framework.exceptions import APIException as RestApiException
from rest_framework.exceptions import NotFound
from zhishuyun_scaffold.settings import ERROR_CODE_API_ERROR, \
    ERROR_DETAIL_API_ERROR, ERROR_DETAIL_NOT_FOUND
import asyncio
import tornado
from zhishuyun_scaffold.handlers.health import HealthHandler


class BaseController(object):

    def __init__(self):
        self.id = str(uuid4())
        self.application = tornado.web.Application([
            (r"/health", HealthHandler),
        ])

    def add_handler(self, path, handler):
        self.application.add_handlers(
            '.*', [(path, handler)])

    async def main(self):
        self.application.listen(HTTP_PORT)
        await asyncio.Event().wait()

    def start(self):
        asyncio.run(self.main())
