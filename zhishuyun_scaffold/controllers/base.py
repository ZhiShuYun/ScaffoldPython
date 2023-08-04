from aiohttp import web
from loguru import logger
from uuid import uuid4
from zhishuyun_scaffold.settings import HTTP_HOST, HTTP_PORT
from rest_framework.exceptions import APIException as RestApiException
from rest_framework.exceptions import NotFound
from zhishuyun_scaffold.settings import ERROR_CODE_API_ERROR, \
    ERROR_DETAIL_API_ERROR, ERROR_DETAIL_NOT_FOUND


class BaseController(object):

    def __init__(self):
        self.id = str(uuid4())
        self.app = web.Application()
        self.handler_class_map = {}
        self.register_routes()

    async def health(self, request):
        # return 200 if server is healthy
        logger.debug('health check')
        return web.Response(text='ok', status=200)

    def get_handler_class_index(self, handler_class):
        return f'{handler_class.method}-{handler_class.path}'

    async def handle(self, request, trace_id=None):
        trace_id = trace_id or str(uuid4())
        logger.debug(f'[{trace_id}] start to handle request')
        handler_class_index = f'{request.method}-{request.path}'
        logger.debug(f'handler class index is {handler_class_index}')
        logger.debug(f'handler_class_map is {self.handler_class_map}')
        response = None
        try:
            handler_class = self.handler_class_map.get(handler_class_index)
            logger.debug(f'[{trace_id}] handler class is {handler_class}')
            if not handler_class:
                raise NotFound(ERROR_DETAIL_NOT_FOUND)
            handler = handler_class(request, trace_id)
            response = await handler.handle()
            return response
        except RestApiException as ex:
            logger.error(f'get rest api exception {ex}')
            return web.json_response(
                {
                    'detail': ex.detail,
                    'code': ex.default_code
                }, status=ex.status_code)
        except Exception:
            logger.exception(f'{trace_id} get general exception')
            response = web.json_response({
                'detail': ERROR_DETAIL_API_ERROR,
                'code': ERROR_CODE_API_ERROR
            }, status=500)
            return response

    def register_routes(self):
        logger.debug('add router for health')
        self.app.router.add_route('GET', '/health', self.health)
        self.app.router.add_route('*', '/{path:.*}', self.handle)

    def register_handlers(self, handler_classes):
        for handler_class in handler_classes:
            handler_class_index = self.get_handler_class_index(handler_class)
            self.handler_class_map[handler_class_index] = handler_class

    def start(self):
        web.run_app(self.app, host=HTTP_HOST, port=HTTP_PORT)
