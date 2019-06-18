import json
from typing import Union
from typing import Dict
from typing import Callable
from ..log import Log


class Response:
    def __init__(self, request, fail_callback: Callable):
        self.request = request
        self.fail_callback = fail_callback

    def _response(self, obj, error: bool = False) -> None:
        # todo check for encryption and encrypt it
        try:
            _response = json.dumps(obj)+"\n"
            if error:
                Log.err(obj)
            self.request.send(_response.encode('utf8'))
        except Exception as e:
            self.fail_callback(e)

    def ok(self, data: Union[str, Dict, None] = None) -> None:
        return self._response({"error": False, "response": data})

    def err(self, message: str = None) -> None:
        return self._response({"error": True, "response": message}, error=True)