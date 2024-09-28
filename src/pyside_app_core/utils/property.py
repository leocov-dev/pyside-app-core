from collections.abc import Callable
from typing import Any, Generic

from typing_extensions import TypeVar

_T = TypeVar("_T", default=type)
_R = TypeVar("_R", default=Any)


class ro_classproperty(Generic[_T, _R]):  # noqa: N801
    def __init__(self, f: Callable[[_T], _R]):
        self.f = f

    def __get__(self, obj: object, owner: _T) -> _R:
        return self.f(owner)
