import tornado
from loguru import logger


class BaseHandler(tornado.web.RequestHandler):

    def initialize_trace_id(self):
        trace_id = self.request.query_arguments.get('trace_id')
        self.trace_id = trace_id[0].decode(
            'utf-8') if trace_id and len(trace_id) > 0 else None
        logger.debug(f'trace id {self.trace_id}')

    def initialize(self):
        self.initialize_trace_id()
