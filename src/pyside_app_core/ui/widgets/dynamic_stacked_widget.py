from PySide6.QtWidgets import QSizePolicy, QStackedWidget, QWidget

from pyside_app_core.mixin.object_name_mixin import ObjectNameMixin


class DynamicStackedWidget(ObjectNameMixin, QStackedWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent=parent)

        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        self.setMinimumHeight(10)
        self.setMaximumHeight(100000)
        self.setContentsMargins(0, 0, 0, 0)
