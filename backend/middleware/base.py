import asyncio
from typing import Callable, List
from django.urls.resolvers import URLPattern


def wrap_middleware(middleware):
    def wraps(func):
        if asyncio.iscoroutinefunction(middleware):
            async def inner(request, *args, **kwargs):
                return await middleware(request, lambda: func(request, *args, **kwargs))
            return inner
        else:
            def inner(request, *args, **kwargs):
                return middleware(request, lambda: func(request, *args, **kwargs))
            return inner
    return wraps


def wrap_path_middleware(middleware: Callable[[Callable], Callable], pathes: List[URLPattern]):
    for path in pathes:
        path.callback = middleware(path.callback)
    return pathes
