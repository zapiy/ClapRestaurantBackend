from django.http import HttpResponse
import orjson

from .json_encoder import custom_json_encoder


class CustomJsonResponse(HttpResponse):
    def __init__(self, data: dict = {}, **kwargs):
        kwargs.setdefault("content_type", "application/json")
        self.data = data
        super().__init__(
            content=orjson.dumps(data, default=custom_json_encoder, option=orjson.OPT_PASSTHROUGH_DATETIME),
            **kwargs
        )
