from typing import Generic, Callable, List
from typing_extensions import ParamSpec
import asyncio


_P = ParamSpec("_P")
class SimpleEvent(Generic[_P], List[Callable[_P, None]]):

    def __class_getitem__(cls, params):
        return cls
    
    @property
    def count(self):
        return len(self)
    
    def __iadd__(self, func: Callable[_P, None]):
        self.append(func)
        return self

    def __isub__(self, func: Callable[_P, None]):
        self.remove(func)
        return self

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs):
        for handler in self:
            res = handler(*args, **kwargs)
            if asyncio.iscoroutine(res):
                asyncio.create_task(res)
