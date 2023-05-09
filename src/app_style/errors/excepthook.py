import sys
import traceback
from types import TracebackType
from typing import Type

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox, QApplication

from app_style import logging


def install_excepthook():
    sys.excepthook = __odc_excepthook


def __odc_excepthook(etype: Type[Exception], evalue: Exception, tb: TracebackType):
    formatted_exception_string = "".join(traceback.format_exception(etype, evalue, tb))

    if hasattr(evalue, "internal"):
        if evalue.internal:
            logging.exception(formatted_exception_string)
            return

    msg_box = QtWidgets.QMessageBox()
    msg_box.setText("<h2>{}</h2>".format(etype.__name__))
    msg_box.setDetailedText(formatted_exception_string)
    msg_box.setStandardButtons(
        QtWidgets.QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Abort
    )
    msg_box.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
    msg_box.setIcon(QtWidgets.QMessageBox.Icon.Critical)

    msg_box.setButtonText(QMessageBox.StandardButton.Abort, "Terminate")

    ret = msg_box.exec()

    if ret == QMessageBox.StandardButton.Abort:
        QApplication.instance().quit()
