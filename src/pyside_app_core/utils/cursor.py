import contextlib
from collections.abc import Generator

from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication


def set_cursor(cursor: Qt.CursorShape) -> None:
    QGuiApplication.setOverrideCursor(cursor)


def clear_cursor() -> None:
    QGuiApplication.restoreOverrideCursor()


@contextlib.contextmanager
def cursor_override(cursor: Qt.CursorShape) -> Generator[None, None, None]:
    set_cursor(cursor)
    yield
    clear_cursor()
