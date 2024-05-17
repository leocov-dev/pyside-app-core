from PySide6 import QtWidgets
from PySide6.QtWidgets import QSizePolicy

from pyside_app_core.qt.widgets.object_name_mixin import ObjectNameMixin


class DynamicStackedWidget(ObjectNameMixin, QtWidgets.QStackedWidget):
    def __init__(self, parent: QtWidgets.QWidget) -> None:
        super().__init__(parent=parent)

        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.setMinimumHeight(10)
        self.setMaximumHeight(100000)
        self.setContentsMargins(0, 0, 0, 0)
