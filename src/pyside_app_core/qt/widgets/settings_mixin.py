from typing import cast

from PySide6.QtCore import QCoreApplication, QObject, QSettings
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QWidget

from pyside_app_core.qt.application_service import AppMetadata


class SettingsMixin:
    def __init__(self, parent: QObject | None = None, *args: object, **kwargs: object):
        super().__init__(*args, **kwargs)

        self._settings = QSettings(
            AppMetadata.id,
            AppMetadata.name,
            parent,
        )

        self._restored = False

        cast(QCoreApplication, QCoreApplication.instance()).aboutToQuit.connect(self._store_state)

    def showEvent(self, event: QShowEvent) -> None:  # noqa: N802
        if not self._restored:
            self._restore_state()
            self._restored = True

        if isinstance(self, QWidget):
            cast(QWidget, super()).showEvent(event)

    def _restore_state(self) -> None:
        pass

    def _store_state(self) -> None:
        pass
