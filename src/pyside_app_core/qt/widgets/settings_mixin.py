import os

from PySide6.QtCore import QCoreApplication, QObject, QSettings
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QWidget

from pyside_app_core.services import application_service


class SettingsMixin:
    def __init__(self, parent: QObject, *args, **kwargs):
        super(SettingsMixin, self).__init__(*args, **kwargs)

        self._settings = QSettings(
            application_service.get_app_id(),
            application_service.get_app_name(),
            parent,
        )

        self._restored = False

        QCoreApplication.instance().aboutToQuit.connect(self._store_state)

    def showEvent(self, event: QShowEvent):
        if not self._restored:
            self._restore_state()
            self._restored = True

        if isinstance(self, QWidget):
            super().showEvent(event)

    def _restore_state(self):
        pass

    def _store_state(self):
        pass
