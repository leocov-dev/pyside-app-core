import sys
import traceback
from types import TracebackType
from typing import Protocol, Type

from PySide6.QtWidgets import QDialog

from pyside_app_core import log


class ErrorDialogInterface(Protocol):
    def __init__(self, message: str, details: str | None = None):
        ...

    def exec(self) -> None:
        ...


_error_dialog_class: Type[ErrorDialogInterface] | None = None


def install_excepthook(error_dialog: Type[QDialog] | None = None) -> None:
    global _error_dialog_class
    _error_dialog_class = error_dialog
    sys.excepthook = __custom_excepthook


def __custom_excepthook(
    etype: Type[BaseException], evalue: BaseException, tb: TracebackType | None
):
    formatted_exception_string = "".join(traceback.format_exception(etype, evalue, tb))

    if hasattr(evalue, "internal"):
        if evalue.internal:
            log.exception(formatted_exception_string)
            return

    if _error_dialog_class:
        _error_dialog_class(
            f"<{etype.__name__}>\n{evalue}", formatted_exception_string
        ).exec()
