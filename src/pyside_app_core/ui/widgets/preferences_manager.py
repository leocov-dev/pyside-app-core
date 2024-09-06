from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QStackedWidget,
    QTreeView, QVBoxLayout, QWidget, QSplitter,
)

from pyside_app_core.services.preferences_service import PreferencesService
from pyside_app_core.ui.widgets.window_settings_mixin import WindowSettingsMixin

_mgr = None


class PreferencesManager(WindowSettingsMixin, QWidget):

    @classmethod
    def open(cls):
        global _mgr
        if _mgr is not None:
            _mgr.close()
            _mgr.deleteLater()

        _mgr = PreferencesManager()
        _mgr.show()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)

        self.setWindowTitle("Preferences")

        # ---
        _ly = QVBoxLayout()
        # _ly.setContentsMargins(0, 0, 0, 0)
        self.setLayout(_ly)

        _split = QSplitter(Qt.Orientation.Horizontal, parent=self)
        _ly.addWidget(_split)

        self._group_list = QTreeView(self)
        self._group_list.setHeaderHidden(True)
        _split.addWidget(self._group_list)

        self._pref_stack = QStackedWidget(self)
        _split.addWidget(self._pref_stack)

        # ---
        _split.setStretchFactor(0, 1)
        _split.setStretchFactor(1, 3)
        self._group_list.setModel(PreferencesService.model())

        # ---
        self._group_list.clicked.connect(self._on_pick)

        self._group_list.setCurrentIndex(
            PreferencesService.model().index(self.get_setting("selected-group-idx", 0, int), 0)
        )

    def _on_pick(self, index: QModelIndex):
        item = PreferencesService.model().itemFromIndex(index)
        print(item)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.store_setting("selected-group-idx", self._pref_stack.currentIndex())
        return super().closeEvent(event)
