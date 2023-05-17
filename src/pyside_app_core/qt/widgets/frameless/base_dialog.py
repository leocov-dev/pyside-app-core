from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QAbstractButton,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from pyside_app_core.qt.widgets.frameless.base_window import FramelessBaseMixin

StandardButton = QDialogButtonBox.StandardButton
ButtonRole = QDialogButtonBox.ButtonRole


class FramelessBaseDialog(FramelessBaseMixin, QDialog):
    clicked = Signal(QAbstractButton)

    def __init__(self, icon: QIcon | None = None):
        super().__init__(parent=None, f=Qt.WindowType.WindowCloseButtonHint)

        self.layout().setContentsMargins(10, 0, 10, 10)
        self.layout().addSpacing(20)

        _margin = 20 if icon else 0

        _div = QHBoxLayout()
        _div.setContentsMargins(_margin, 0, _margin, 0)
        self.layout().addLayout(_div)

        if icon:
            _icon = QLabel(parent=self)
            _icon.setFixedSize(64, 64)
            _icon.setPixmap(icon.pixmap(64, 64))
            _div.addWidget(_icon, alignment=Qt.AlignmentFlag.AlignTop)

        self._info = QVBoxLayout()
        self._info.setContentsMargins(_margin, 0, 0, 0)
        _div.addLayout(self._info)

        self._button_box = QDialogButtonBox()
        self._button_box.rejected.connect(self.reject)
        self._button_box.accepted.connect(self.accept)
        self._button_box.clicked.connect(self.clicked.emit)

        self.layout().addWidget(self._button_box)

    def addWidget(self, widget: QWidget, *args, **kwargs) -> None:
        self._info.addWidget(widget, *args, **kwargs)

    def addStretch(self, val: int = 0):
        self._info.addStretch(val)

    def setStandardButtons(self, buttons: StandardButton):
        self._button_box.setStandardButtons(buttons)

    def setDefaultButton(self, button: StandardButton):
        std_button = self.button(button)
        std_button.setDefault(True)

    def setButtonText(self, button: StandardButton, text: str):
        std_button = self.button(button)
        std_button.setText(text)

    def button(self, button: StandardButton) -> QPushButton | None:
        return self._button_box.button(button)

    def buttonRole(self, button: QAbstractButton) -> ButtonRole:
        return self._button_box.buttonRole(button)
