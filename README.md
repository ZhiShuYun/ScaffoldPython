# ZhiShuYun Scaffold

Install:

```
pip install "zhishuyun['scaffold']"
```

Sample:


```python
from zhishuyun_scaffold import BaseController as Controller
from zhishuyun_scaffold import BaseHandler
from aiohttp import web


class Handler(BaseHandler):

    method = 'POST'
    path = '/hello'

    async def handle(self):
        result = {
            'value': 'hello'
        }
        return web.json_response(result, status=200)


controller = Controller()
controller.register_handlers([Handler])

controller.start()

```