from PySide6.QtCore import SignalInstance
from PySide6.QtWidgets import QLineEdit


class PrefCheckBox(QLineEdit):
    def setValue(self, value: str) -> None:
        self.setText(value)

    @property
    def valueChanged(self) -> SignalInstance:
        return self.textChanged
