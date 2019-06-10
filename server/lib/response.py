import json

class Response:
    def __init__(self, response=None, error=None):
        self.set_response(response)
        self.set_error(error)

    def set_response(self, response):
        self.response = response

    def set_error(self, error):
        self.error = error

    def __str__(self):
        if self.error is not None:
            return json.dumps({"error": self.error}) + "\n"
        return json.dumps({"response": self.response}) + "\n"


