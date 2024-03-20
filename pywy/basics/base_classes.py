from typing import Any, Dict, List, Callable
from functools import partial, wraps


class ImmutableError(Exception):
    def __init__(self, attr_protected: str) -> None:
        message = f"Operation not allowed. Attribute {attr_protected} can not set."
        super().__init__(message)


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwags) -> "Singleton":
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


class Immutable:
    def __init__(self, *args) -> None:
        self._protected_paramns = args
        # for paramn in self._protected_paramns:
        #     self.__setattr__()

    def __setattr__(self, __name: str, __value: Any) -> None:
        if self._is_frozen(__name):
            tb = ImmutableError(__name).__traceback__
            raise ImmutableError(attr_protected=__name).with_traceback(tb)
        self.__dict__[__name] = __value

    def _is_frozen(self, __name) -> bool:
        return __name in self.__dict__ and __name in self._protected_paramns
