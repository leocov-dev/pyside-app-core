import inspect
import logging
from collections.abc import Callable
from typing import Protocol

__logger_cache: dict[str, logging.Logger] = {}

__pac_name = "pyside_app_core"


def _get_caller_name() -> str:
    try:
        stack = inspect.stack()
        frame = stack[2][0]
        module = inspect.getmodule(frame)
        if not module:
            return __pac_name
    except:  # noqa
        return __pac_name
    name = module.__name__
    if name == "__main__":
        name = __pac_name

    return name


def _get_cached_logger(name: str) -> logging.Logger:
    if name in __logger_cache:
        lg = __logger_cache[name]
    else:
        lg = logging.getLogger(name)
        __logger_cache[name] = lg

    return lg


class _Logger(Protocol):
    def debug(self, msg: str, /, *args: object, **kwargs: object) -> None: ...

    def info(self, msg: str, /, *args: object, **kwargs: object) -> None: ...

    def warning(self, msg: str, /, *args: object, **kwargs: object) -> None: ...

    def error(self, msg: str, /, *args: object, **kwargs: object) -> None: ...

    def critical(self, msg: str, /, *args: object, **kwargs: object) -> None: ...

    def exception(self, msg: str, /, *args: object, **kwargs: object) -> None: ...


def __default_get_logger() -> logging.Logger:
    name = _get_caller_name()
    return _get_cached_logger(name)


GetLogger = Callable[[], _Logger]

__get_logger_func: GetLogger = __default_get_logger  # type: ignore[assignment]


def configure_get_logger_func(func: GetLogger) -> None:
    global __get_logger_func  # noqa: PLW0603
    __get_logger_func = func


def debug(msg: object, *args: object, **kwargs: object) -> None:
    """call logger's debug"""
    lg = __get_logger_func()
    lg.debug(msg, *args, **kwargs)  # type: ignore[arg-type]


def info(msg: object, *args: object, **kwargs: object) -> None:
    """call logger's info"""
    lg = __get_logger_func()
    lg.info(msg, *args, **kwargs)  # type: ignore[arg-type]


def warning(msg: object, *args: object, **kwargs: object) -> None:
    """call logger's warning"""
    lg = __get_logger_func()
    lg.warning(msg, *args, **kwargs)  # type: ignore[arg-type]


def error(msg: object, *args: object, **kwargs: object) -> None:
    """call logger's error"""
    lg = __get_logger_func()
    lg.error(msg, *args, **kwargs)  # type: ignore[arg-type]


def critical(msg: object, *args: object, **kwargs: object) -> None:
    """call logger's critical"""
    lg = __get_logger_func()
    lg.critical(msg, *args, **kwargs)  # type: ignore[arg-type]


def exception(msg: object, *args: object, **kwargs: object) -> None:
    """call logger's exception"""
    lg = __get_logger_func()
    lg.exception(msg, *args, **kwargs)  # type: ignore[arg-type]
