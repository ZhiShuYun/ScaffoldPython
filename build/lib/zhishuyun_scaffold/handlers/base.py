from uuid import uuid4


class BaseHandler(object):

    def __init__(self, request, trace_id=None):
        self.request = request
        self.trace_id = trace_id or str(uuid4())
