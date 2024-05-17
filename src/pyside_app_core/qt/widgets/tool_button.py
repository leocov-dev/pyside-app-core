from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton, QWidget

from pyside_app_core.qt.widgets.object_name_mixin import ObjectNameMixin


class ToolButton(ObjectNameMixin, QPushButton):
    def __init__(self, icon: QIcon, tooltip: str, parent: QWidget):
        super().__init__(icon=icon, parent=parent)

        self.setMinimumSize(24, 24)

        self.setToolTip(tooltip)
        self.setContentsMargins(0, 0, 0, 0)

    def setFixedSize(  # type: ignore[override] # noqa
        self, size: QSize | tuple[int, int]
    ) -> None:
        if isinstance(size, tuple):
            size = QSize(size[0], size[1])
        super().setFixedSize(size + QSize(10, 10))
        self.setIconSize(size)
