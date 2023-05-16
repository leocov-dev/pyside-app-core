from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMainWindow

from pyside_app_core.qt.widgets.object_name_mixin import ObjectNameMixin
from pyside_app_core.qt.widgets.settings_mixin import SettingsMixin


class WindowSettingsMixin(ObjectNameMixin, SettingsMixin):
    def __init__(self, parent: QObject, *args, **kwargs):
        super(WindowSettingsMixin, self).__init__(parent=parent, *args, **kwargs)

    def _store_state(self) -> None:
        self._settings.setValue(f"{self.obj_name}_geometry", self.saveGeometry())

        if isinstance(self, QMainWindow):
            self._settings.setValue(f"{self.obj_name}_window_state", self.saveState())

    def _restore_state(self) -> None:
        self.restoreGeometry(self._settings.value(f"{self.obj_name}_geometry"))

        # if isinstance(self, QMainWindow):
        #     self.restoreState(self._settings.value(f"{self.obj_name}_window_state"))
