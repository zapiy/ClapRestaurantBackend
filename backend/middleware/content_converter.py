from typing import Callable
from django.http import HttpRequest, HttpResponse
import orjson


class ContentTypeConverterMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        try:
            if request.method != 'GET' and request.content_type == "application/json":
                request.POST = orjson.loads(request.body)
        except:
            request.POST = {}
            
        return self.get_response(request)
    