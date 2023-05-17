import sys
import traceback
from types import TracebackType
from typing import Type

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox, QApplication

from pyside_app_core import log
from pyside_app_core.qt.widgets.error_dialog import ErrorDialog


def install_excepthook():
    sys.excepthook = __custom_excepthook


def __custom_excepthook(etype: Type[Exception], evalue: Exception, tb: TracebackType):
    formatted_exception_string = "".join(traceback.format_exception(etype, evalue, tb))

    if hasattr(evalue, "internal"):
        if evalue.internal:
            log.exception(formatted_exception_string)
            return

    error_dialog = ErrorDialog(
        f"<{etype.__name__}>\n{evalue}", formatted_exception_string
    )

    error_dialog.exec()
