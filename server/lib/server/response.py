import json
from ..log import Log


class Response:
    def __init__(self, request, fail_callback):
        self.request = request
        self.fail_callback = fail_callback

    def _response(self, obj, error=False):
        try:
            _response = json.dumps(obj)+"\n"
            if error:
                Log.err(obj)
            self.request.send(_response.encode('utf8'))
        except Exception as e:
            self.fail_callback(e)

    def ok(self, data=None):
        self._response({"error": False, "response": data})

    def err(self, message=None):
        self._response({"error": True, "response": message}, error=True)