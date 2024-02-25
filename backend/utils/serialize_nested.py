from typing import Callable, Dict, Optional, Type, TypeVar, Union
from types import LambdaType, FunctionType, GeneratorType
from copy import deepcopy
from dataclasses import dataclass
from collections import namedtuple

_is_list = lambda val: isinstance(val, (list, GeneratorType))
_is_primitive = lambda val: isinstance(val, (bool, str, int, float, type(None)))


_T = TypeVar("_T")
@dataclass
class SNF:
    cast: Type[_T]
    null: bool = False
    default: Union[_T, Callable[[], _T]] = None
    validate: Callable[[_T], bool] = None
    prepare: Callable[[_T], _T] = None
    limit: range = None


class SN:
    def __init__(self, *fields: str, **extra: Dict[str, Union[str, 'SN', SNF]]) -> None:
        assert fields or extra, "'fields' and 'extra' cannot be empty both"
        
        self.__fields = list(fields)
        self.__extra = deepcopy(extra)
        self.__cached = {}
        
        form = {
            k: v
            for k, v in extra.items()
            if isinstance(v, SNF)
        }
        if form:
            self.__fields.extend(form.keys())
            for f in form:
                self.__extra.pop(f)
        
        for f in list(self.__fields):
            if not f.startswith('_'): continue
            self.__fields.remove(f)
            form[f] = None
        
        self.__form = form
        
    def extend(self, other: 'SN'):
        assert isinstance(other, SN)
        return SN(
            *{*deepcopy(other.__fields), *deepcopy(self.__fields)},
            **{**other.__extra, **self.__extra},
        )
        
    def copy(self):
        return SN(*deepcopy(self.__fields), **deepcopy(self.__extra))
    
    def __import(self, type: Type[_T]):
        mapping = self
        for f in list(self.__fields):
            if not f.startswith("$"): continue
            target_map = getattr(type, f"SN_{f[1:]}", None)
            if not isinstance(target_map, SN):
                raise Exception(f"Type {type} has no mapping '{f}' to extend")
            
            mapping = mapping.extend(target_map)
            mapping.__cached = self.__cached
        return mapping
    
    def serialize(self, obj: Union[_T, list]) -> dict:
        mapping = self
        if _is_primitive(obj) or isinstance(obj, dict):
            return obj
        
        if hasattr(obj, "all") and isinstance(getattr(obj, 'all'), Callable):
            obj = list(obj.all())
        if not _is_primitive(obj) and _is_list(obj):
            return [self.serialize(el) for el in obj]
        
        if type(obj) in self.__cached:
            mapping = self.__cached[type(obj)]
        else:
            self.__cached[type(obj)] = mapping = mapping.__import(type(obj))
                    
        output = {}
        for f in mapping.__fields:
            if f.startswith("$"): continue
            elif not hasattr(obj, f):
                raise Exception(f"Type {type(obj)} has no attribute '{f}'")
            
            parsed = getattr(obj, f)
            if type(parsed) in self.__cached or _is_list(parsed):
                output[f] = self.serialize(parsed)
            else:
                output[f] = parsed
            
        for field, value in mapping.__extra.items():
            if isinstance(value, str):
                if not hasattr(obj, value):
                    raise Exception(f"Type {type(obj)} has no attribute '{value}'")
                
                parsed = getattr(obj, value)
                if type(parsed) in self.__cached or _is_list(parsed):
                    output[field] = self.serialize(parsed)
                else:
                    output[field] = parsed
                continue
            
            elif isinstance(value, (LambdaType, FunctionType)):
                output[field] = (value(getattr(obj, field)) if hasattr(obj, field) else value(obj))
            
            if isinstance(value, SN):
                if not hasattr(obj, field):
                    raise Exception(f"Type {type(obj)} has no attribute '{field}'")
                parsed = getattr(obj, field)
                    
                if not isinstance(parsed, object):
                    raise Exception(f"Type {type(obj)} attribute '{field}' use tree view, but value no object")
                
                if type(parsed) in self.__cached:
                    output[field] = self.__cached[type(parsed)].serialize(parsed)
                else:
                    output[field] = value.serialize(parsed)
            
            elif (
                isinstance(value, tuple) and len(value) == 2 
                and isinstance(value[0], str) and isinstance(value[1], LambdaType)
            ):
                if not hasattr(obj, value[0]):
                    raise Exception(f"Type {type(obj)} has no attribute '{value[0]}'")
                
                output[field] = value[1](getattr(obj, value[0]))

        return output
    
    def parse(
        self, src: dict, 
        obj: Optional[Union[Type[_T], _T]] = None,
    ) -> _T:
        assert self.__form
        form = self.__form.copy()

        if obj:
            type_ = (obj if isinstance(obj, type) else type(obj))
            
            for f in list(form.keys()):
                if not f.startswith('_'): continue
                target_map = getattr(obj, f"SN_{f[1:]}", None)
                if not isinstance(target_map, SN):
                    raise Exception(f"Type {type_} has no mapping '{f}' to extend")
                elif not target_map.__form:
                    raise Exception(f"Type {type_} has no form fields to extend")
                
                form.pop(f)
                form.update(target_map.__form)
                
        parsed = {}
        
        if isinstance(obj, type):
            obj = obj()
        
        for k, extra in form.items():
            if k.startswith('_'): continue
            val = self.safe_get(src, k, extra=extra)
            if (
                val is not None 
                or extra.null
            ):
                parsed[k] = val
            elif (
                obj is None
                or getattr(obj, k) is None
            ):
                return None
        
        if obj is None:
            return namedtuple('SNGenerated', parsed.keys())(**parsed)
        
        for k, v in parsed.items():
            setattr(obj, k, v)
        
        return obj
    
    @staticmethod
    def safe_get(src: dict, key: str, extra: SNF):
        try:
            value = src[key]
            if extra.null or value is not None:
                if extra.cast == bool and isinstance(value, str):
                    if value.lower() in ["true", "1", "yes"]:
                        return True
                    elif value.lower() in ["false", "0", "no"]:
                        return False
                    elif extra.default is None:
                        return False
                else:
                    value = extra.cast(value)
                    if extra.cast == str:
                        value = value.strip()
                    
                    if (
                        extra.limit is not None
                        and (
                            (extra.cast == str and len(value) not in extra.limit)
                            or (
                                (extra.cast == int or extra.cast == float)
                                and value not in extra.limit
                            )
                        )
                    ):
                        raise ValueError()
                    
                    if extra.validate is None or extra.validate(value):
                        return (extra.prepare(value) if extra.prepare else value)
                    
        except (KeyError, ValueError, TypeError):
            pass
        if isinstance(extra.default, Callable):
            return extra.default()
        return extra.default
    
    def __str__(self) -> str:
        return f"<SN ({self.__fields}) {self.__extra}>" 

    def __repr__(self) -> str:
        return str(self)

