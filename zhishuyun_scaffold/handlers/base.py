import tornado
from loguru import logger
from zhishuyun_scaffold.exceptions import APIException
import json
from zhishuyun_scaffold.settings import ERROR_CODE_UNKNOWN, GATEWAY_SERVER_URL
from uuid import uuid4
import requests
from urllib.parse import urljoin


class BaseHandler(tornado.web.RequestHandler):

    # override for default behavior, do not use this method
    def send_error(self, status_code: int = 500, **kwargs):
        self.write_error(status_code, **kwargs)

    def set_default_headers(self):
        self.set_header("Content-Type", 'application/json')

    def write_json(self, data_json):
        self.write(json.dumps(data_json, ensure_ascii=False))

    @logger.catch
    def send_callback(self, data):
        logger.debug(f'{self.trace_id} callback url {self.callback_url}')
        logger.debug(f'{self.trace_id} callback data {data}')
        response = requests.post(self.callback_url, json=data)
        logger.debug(f'{self.trace_id} callback response {response}')

    @logger.catch
    def send_record(self, data):
        record_url = urljoin(GATEWAY_SERVER_URL, '/record')
        logger.debug(f'{self.trace_id} record url {record_url}')
        data = {
            **data,
            'trace_id': self.trace_id,
            'application_id': self.application_id,
            'metadata': {
                'task_id': self.task_id,
            }
        }
        logger.debug(f'{self.trace_id} record data {data}')
        response = requests.post(record_url, json=data)
        logger.debug(f'{self.trace_id} record response {response}')

    def write_success(self, data, status=200):
        data['success'] = True if status < 400 else False
        data['task_id'] = self.task_id
        if self.async_mode:
            self.send_callback(data)
            self.send_record({**data, 'status': status})
        else:
            self.write_json(data)
            self.finish()
            logger.debug(f'{self.trace_id} write json {data}')

    def write_error(self, status, **kwargs):
        logger.error(f'error happened {kwargs}')
        exception = None
        if "exc_info" in kwargs:
            exception = kwargs["exc_info"][1]
        logger.error(f'error {exception}')
        data = {}
        status = status or exception.status_code if hasattr(
            exception, 'status_code') else 500
        logger.debug(f'{self.trace_id} error status {status}')
        # construct error
        if isinstance(exception, APIException):
            data = {
                'task_id': self.task_id,
                'success': False,
                'code': exception.code,
                'detail': exception.detail,
            }
        else:
            data = {
                'task_id': self.task_id,
                'success': False,
                'code': ERROR_CODE_UNKNOWN,
                'detail': str(exception),
            }
        if self.async_mode:
            self.send_callback(data)
            self.send_record({**data, 'status': status})
        else:
            self.set_status(status)
            self.write_json(data)
            self.finish()
            logger.debug(f'{self.trace_id} write error {data}')

    def initialize_trace_id(self):
        trace_id = self.request.query_arguments.get('trace_id')
        self.trace_id = trace_id[0].decode(
            'utf-8') if trace_id and len(trace_id) > 0 else None
        logger.debug(f'trace id {self.trace_id}')

    def initialize_application_id(self):
        application_id = self.request.query_arguments.get('application_id')
        self.application_id = application_id[0].decode(
            'utf-8') if application_id and len(application_id) > 0 else None
        logger.debug(f'application id {self.application_id}')

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
        self.initialize_application_id()
        self.initialize_async_context()
