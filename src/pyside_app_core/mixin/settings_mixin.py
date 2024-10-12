from typing import Any, TypeVar, cast

from PySide6.QtCore import QCoreApplication, QObject, QSettings
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QWidget

from pyside_app_core import log

_SV = TypeVar("_SV")


class SettingsMixin:
    def __init__(self, *args: object, parent: QObject | None = None, **kwargs: object):
        super().__init__(*args, **kwargs)

        self._settings = QSettings(parent)

        self._restored = False

        cast(QCoreApplication, QCoreApplication.instance()).aboutToQuit.connect(self._store_state)

    def get_setting(
        self,
        key: str,
        default: _SV | None = None,
        type_: type[_SV] | None = None,
    ) -> _SV:
        if type_ is None:
            value = cast(_SV, self._settings.value(key, default))
        else:
            value = cast(_SV, self._settings.value(key, default, type_))

        log.debug(f"get_setting: {key} <= {value}")
        return value

    def store_setting(self, key: str, value: Any) -> None:
        log.debug(f"store_setting: {key} => {value}")
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
