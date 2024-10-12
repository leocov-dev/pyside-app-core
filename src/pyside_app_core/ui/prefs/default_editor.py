from typing import cast

from PySide6.QtWidgets import QFormLayout, QLabel, QVBoxLayout, QWidget

from pyside_app_core.services.preferences_service import PrefGroup


class DefaultPreferencesPage(QWidget):
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)

        _ly = QVBoxLayout()
        self.setLayout(_ly)

        self._heading = QLabel("", self)
        font = self._heading.font()
        font.setBold(True)
        font.setPointSizeF(font.pointSizeF() * 1.25)
        self._heading.setFont(font)
        _ly.addWidget(self._heading)

        _ly.addSpacing(20)

        self._form = QFormLayout()
        self._form.setContentsMargins(15, 0, 0, 0)
        _ly.addLayout(self._form)

        _ly.addStretch(99)

    def set_group(self, group: PrefGroup) -> None:
        self._clear()

        self._heading.setText(group.display_name)

        for item in group:
            self._form.addRow(item.display_name, cast(QWidget, item.widget_class(item, self)))

    def _clear(self) -> None:
        while child := self._form.takeAt(0):
            if w := child.widget():
                w.deleteLater()
            del child
