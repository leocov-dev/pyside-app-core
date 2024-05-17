from typing import cast

from PySide6.QtCore import QByteArray, QObject
from PySide6.QtWidgets import QMainWindow, QWidget

from pyside_app_core.qt.widgets.object_name_mixin import ObjectNameMixin
from pyside_app_core.qt.widgets.settings_mixin import SettingsMixin


class WindowSettingsMixin(ObjectNameMixin, SettingsMixin):
    def __init__(self, parent: QObject | None = None, *args: object, **kwargs: object) -> None:
        super().__init__(*args, parent=parent, **kwargs)

    def _store_state(self) -> None:
        self._settings.setValue(f"{self.obj_name}_geometry", cast(QWidget, self).saveGeometry())

        if isinstance(self, QMainWindow):
            cast(SettingsMixin, self)._settings.setValue(  # noqa: SLF001
                f"{cast(ObjectNameMixin, self).obj_name}_window_state", self.saveState()
            )

    def _restore_state(self) -> None:
        cast(QWidget, self).restoreGeometry(cast(QByteArray, self._settings.value(f"{self.obj_name}_geometry")))

        if isinstance(self, QMainWindow):
            self.restoreState(cast(QByteArray, self._settings.value(f"{self.obj_name}_window_state")))
