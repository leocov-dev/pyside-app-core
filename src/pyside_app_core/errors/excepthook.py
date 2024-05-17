import sys
import traceback
from types import TracebackType
from typing import Protocol

from PySide6.QtWidgets import QDialog

from pyside_app_core import log


class ErrorDialogInterface(Protocol):
    def __init__(self, etype: type[BaseException], message: str, details: str | None = None): ...

    def exec(self) -> int: ...


_error_dialog_class: type[ErrorDialogInterface] | None = None


def install_excepthook(error_dialog: type[QDialog] | None) -> None:
    global _error_dialog_class  # noqa
    _error_dialog_class = error_dialog
    sys.excepthook = __custom_excepthook


def __custom_excepthook(
    etype: type[BaseException],
    evalue: BaseException,
    tb: TracebackType | None,
) -> None:
    formatted_exception_string = "".join(traceback.format_exception(etype, evalue, tb))

    log.exception(formatted_exception_string)

    if hasattr(evalue, "internal") and evalue.internal:
        return

    if _error_dialog_class:
        _error_dialog_class(etype, str(evalue), formatted_exception_string).exec()
