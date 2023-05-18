import inspect
import logging
from typing import Dict

from pyside_app_core.log.logger import PACLogger

__logger_cache: Dict[str, logging.Logger] = {}

logging.setLoggerClass(PACLogger)

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


def set_level(name: str = None, lvl: int = None):
    """set the logger level"""
    if not name:
        name = _get_caller_name()
    if not lvl:
        raise ValueError(f"Please set '{name}' logger level explicitly.")
    lg = _get_cached_logger(name)
    lg.setLevel(lvl)


def debug(msg, *args, **kwargs):
    """call logger's debug"""
    name = _get_caller_name()
    lg = _get_cached_logger(name)
    lg.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """call logger's info"""
    name = _get_caller_name()
    lg = _get_cached_logger(name)
    lg.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    """call logger's warning"""
    name = _get_caller_name()
    lg = _get_cached_logger(name)
    lg.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """call logger's error"""
    name = _get_caller_name()
    lg = _get_cached_logger(name)
    lg.error(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    """call logger's critical"""
    name = _get_caller_name()
    lg = _get_cached_logger(name)
    lg.critical(msg, *args, **kwargs)


def exception(msg, *args, **kwargs):
    """call logger's exception"""
    name = _get_caller_name()
    lg = _get_cached_logger(name)
    lg.exception(msg, *args, **kwargs)


def set_all_level(lvl: int):
    """set level of all loggers"""
    for _, lg in sorted(__logger_cache):
        if not isinstance(lg, PACLogger):
            continue
        lg.setLevel(lvl)
