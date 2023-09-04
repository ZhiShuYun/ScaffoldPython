import tornado
from loguru import logger
from zhishuyun_scaffold.exceptions import APIException
import json
from zhishuyun_scaffold.settings import ERROR_CODE_UNKNOWN


class BaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def write_json(self, data):
        self.write(json.dumps(data))

    def write_error(self, status_code, **kwargs):
        exception = None
        if "exc_info" in kwargs:
            exception = kwargs["exc_info"][1]
        print(exception)
        if isinstance(exception, APIException):
            result = {
                'code': exception.code,
                'detail': exception.detail,
            }
            self.set_status(exception.status_code)
            self.write(json.dumps(result))
            self.finish()
        else:
            result = {
                'code': ERROR_CODE_UNKNOWN,
                'detail': str(exception),
            }
            self.set_status(500)
            self.write(json.dumps(result))
            self.finish()

    def initialize_trace_id(self):
        trace_id = self.request.query_arguments.get('trace_id')
        self.trace_id = trace_id[0].decode(
            'utf-8') if trace_id and len(trace_id) > 0 else None
        logger.debug(f'trace id {self.trace_id}')

    def initialize(self):
        self.initialize_trace_id()
