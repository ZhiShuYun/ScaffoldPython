import tornado
from loguru import logger
from zhishuyun_scaffold.exceptions import APIException
import json
from zhishuyun_scaffold.settings import ERROR_CODE_UNKNOWN
from uuid import uuid4
import requests


class BaseHandler(tornado.web.RequestHandler):

    # override for default behavior, do not use this method
    def send_error(self, status_code: int = 500, **kwargs):
        self.write_error(status_code, **kwargs)

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def write_json(self, data_json):
        self.write(json.dumps(data_json, ensure_ascii=False))

    def write_success(self, success_json):
        success_json['success'] = True
        success_json['task_id'] = self.task_id
        if self.async_mode:
            response = requests.post(self.callback_url, json=success_json)
            logger.debug(f'{self.trace_id} callback response {response}')
        else:
            self.write_json(success_json)
            self.finish()
            logger.debug(f'{self.trace_id} write json {success_json}')

    def write_error(self, status_code, **kwargs):
        logger.error(f'error happened {kwargs}')
        exception = None
        if "exc_info" in kwargs:
            exception = kwargs["exc_info"][1]
        logger.error(f'error {exception}')
        error_json = {}
        # construct error
        if isinstance(exception, APIException):
            error_json = {
                'task_id': self.task_id,
                'success': False,
                'code': exception.code,
                'detail': exception.detail,
            }
        else:
            error_json = {
                'task_id': self.task_id,
                'success': False,
                'code': ERROR_CODE_UNKNOWN,
                'detail': str(exception),
            }
        if self.async_mode:
            response = requests.post(self.callback_url, json=error_json)
            logger.debug(f'{self.trace_id} callback response {response}')
        else:
            self.set_status(exception.status_code if hasattr(
                exception, 'status_code') else 500)
            self.write_json(error_json)
            self.finish()
            logger.debug(f'{self.trace_id} write error {error_json}')

    def initialize_trace_id(self):
        trace_id = self.request.query_arguments.get('trace_id')
        self.trace_id = trace_id[0].decode(
            'utf-8') if trace_id and len(trace_id) > 0 else None
        logger.debug(f'trace id {self.trace_id}')

    def initialize_task_id(self):
        self.task_id = str(uuid4())
        logger.debug(f'task id {self.task_id}')

    def initialize_async_context(self):
        try:
            request_body = self.request.body.decode('utf-8')
            post_json = json.loads(request_body)
            callback_url = post_json.get('callback_url')
            if callback_url:
                self.async_mode = True
                self.callback_url = callback_url
            else:
                self.async_mode = False
                self.callback_url = None
        except Exception:
            pass

    def initialize(self):
        self.initialize_trace_id()
        self.initialize_task_id()
        self.initialize_async_context()
