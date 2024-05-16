from typing import Protocol

from PySide6.QtCore import QFile, QTextStream


class CanSetStyleSheet(Protocol):
    def setStyleSheet(self, stylesheet: str) -> None:
        ...


def apply_style_sheet(qss_file: str, widget: CanSetStyleSheet) -> None:
    qfile = QFile(qss_file)
    qfile.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text)
    ts = QTextStream(qfile)
    widget.setStyleSheet(ts.readAll())
