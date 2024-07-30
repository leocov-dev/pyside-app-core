from PySide6.QtCore import SignalInstance
from PySide6.QtWidgets import QCheckBox


class PrefCheckBox(QCheckBox):
    def setValue(self, value: bool) -> None:
        self.setChecked(value)

    @property
    def valueChanged(self) -> SignalInstance:
        return self.toggled
