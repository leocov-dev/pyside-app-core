from typing import Type

from pyside_app_core.errors.basic_errors import ApplicationError
from pyside_app_core.qt.style import QssTheme

__app_name = ""
__app_id = ""
__app_version = ""
__app_theme = None


def set_app_name(app_name: str) -> None:
    global __app_name
    if __app_name:
        raise ApplicationError("Can't update app_name after its been set once.")

    __app_name = app_name


def set_app_id(app_id: str) -> None:
    global __app_id
    if __app_id:
        raise ApplicationError("Can't update app_id after its been set once.")

    __app_id = app_id


def set_app_version(app_version: str) -> None:
    global __app_version
    if __app_version:
        raise ApplicationError("Can't update app_version after its been set once.")

    __app_version = app_version


def set_app_theme(app_theme: QssTheme | Type[QssTheme]) -> None:
    global __app_theme
    if __app_theme:
        raise ApplicationError("Can't update app_theme after its been set once.")

    __app_theme = app_theme


def get_app_name() -> str:
    global __app_name
    if not __app_name:
        raise ApplicationError("app_name is unset")
    return __app_name


def get_app_id() -> str:
    global __app_id
    if not __app_id:
        raise ApplicationError("app_id is unset")
    return __app_id


def get_app_version() -> str:
    global __app_version
    if not __app_version:
        raise ApplicationError("app_version is unset")
    return __app_version


def get_app_theme() -> QssTheme:
    global __app_theme
    if not __app_theme:
        raise ApplicationError("app_theme is unset")
    return __app_theme
