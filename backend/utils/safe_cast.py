from typing import Callable, Type, Union, TypeVar


_T = TypeVar("_T")
def safe_cast(val, to: Type[_T], default: Union[_T, Callable[[], _T]]):
    try:
        return to(val)
    except (ValueError, TypeError):
        if isinstance(default, Callable):
            return default()
    return default


def dict_safe_get(
    src: dict, key: str, cast: Type[_T], *,
    allow_null: bool = False, 
    default: Union[_T, Callable[[], _T]] = None, 
    validate: Callable[[_T], bool] = None,
    prepare: Callable[[_T], _T] = None,
):
    try:
        value = src[key]
        if allow_null or value is not None:
            if cast == bool and isinstance(value, str):
                if value.lower() in ["true", "1", "yes"]:
                    return True
                elif value.lower() in ["false", "0", "no"]:
                    return False
                elif default is None:
                    return False
            else:
                value = cast(value)
                if cast == str:
                    value = value.strip()
                if validate is None or validate(value):
                    return (prepare(value) if prepare else value)
    except (KeyError, ValueError, TypeError):
        pass
    if isinstance(default, Callable):
        return default()
    return default
