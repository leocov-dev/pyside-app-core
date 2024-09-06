from typing import Any, cast, TypeVar

from PySide6.QtCore import QCoreApplication, QObject, QSettings
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QWidget

_SV = TypeVar("_SV")


class SettingsMixin:
    def __init__(self, parent: QObject | None = None, *args: object, **kwargs: object):
        super().__init__(*args, **kwargs)

        self._settings = QSettings(parent)

        self._restored = False

        cast(QCoreApplication, QCoreApplication.instance()).aboutToQuit.connect(self._store_state)

    def get_setting(self, key: str, default: _SV | None = None, type_: type[_SV] | None = None) -> _SV:
        if type_ is None:
            return cast(_SV, self._settings.value(key, default))
        return cast(_SV, self._settings.value(key, default, type_))

    def store_setting(self, key: str, value: Any) -> None:
        self._settings.setValue(key, value)

    def showEvent(self, event: QShowEvent) -> None:
        if not self._restored:
            self._restore_state()
            self._restored = True

        if isinstance(self, QWidget):
            cast(QWidget, super()).showEvent(event)

    def _restore_state(self) -> None:
        pass

    def _store_state(self) -> None:
        pass
