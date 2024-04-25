import inspect
import logging
from typing import Callable, Dict

from pyside_app_core.log.logger import PACLogger

__logger_cache: Dict[str, logging.Logger] = {}

# logging.setLoggerClass(PACLogger)

__pac_name = "pyside_app_core"


def _get_caller_name():
    try:
        stack = inspect.stack()
        frame = stack[2][0]
        module = inspect.getmodule(frame)
        if not module:
            return __pac_name
    except:
        return __pac_name
    name = module.__name__
    if name == "__main__":
        name = __pac_name

    return name


def _get_cached_logger(name):
    if name in __logger_cache:
        lg = __logger_cache[name]
    else:
        lg = logging.getLogger(name)
        __logger_cache[name] = lg

    return lg


def __default_get_logger():
    name = _get_caller_name()
    return _get_cached_logger(name)


__get_logger_func = __default_get_logger


def configure_get_logger_func(func: Callable):
    global __get_logger_func
    __get_logger_func = func


def set_level(lvl: int):
    """set the logger level"""
    lg = __get_logger_func()
    lg.setLevel(lvl)


def debug(msg, *args, **kwargs):
    """call logger's debug"""
    lg = __get_logger_func()
    lg.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """call logger's info"""
    lg = __get_logger_func()
    lg.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """call logger's warning"""
    lg = __get_logger_func()
    lg.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """call logger's error"""
    lg = __get_logger_func()
    lg.error(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    """call logger's critical"""
    lg = __get_logger_func()
    lg.critical(msg, *args, **kwargs)


def exception(msg, *args, **kwargs):
    """call logger's exception"""
    lg = __get_logger_func()
    lg.exception(msg, *args, **kwargs)


# def set_all_level(lvl: int):
#     """set level of all loggers"""
#     for key in sorted(__logger_cache.keys()):
#         lg = __logger_cache[key]
#         if not isinstance(lg, PACLogger):
#             continue
#         lg.setLevel(lvl)
