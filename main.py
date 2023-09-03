from zhishuyun_scaffold import BaseController as Controller
from zhishuyun_scaffold import BaseHandler
import json
from zhishuyun_scaffold.exceptions import BadRequestException


class Handler(BaseHandler):

    async def get(self, id=None):
        result = {
            'value': id
        }
        raise BadRequestException('bad')
        self.write(json.dumps(result))


controller = Controller()
controller.add_handler(r'/test/(.*)', Handler)

controller.start()
