from typing import Any

from PySide6.QtCore import QCoreApplication, QObject, Signal

from pyside_app_core.mixin.settings_mixin import SettingsMixin
from pyside_app_core.types.preferences import Pref, PrefsConfig, PrefsGroup, PrefsValue


class PreferencesService(SettingsMixin, QObject):
    pref_changed = Signal(str, PrefsValue)  # type: ignore[arg-type]

    def __new__(cls) -> "PreferencesService":
        if hasattr(cls, "_instance"):
            raise TypeError(f"Get the instance via {cls.__name__}.instance()")

        cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def instance(cls) -> "PreferencesService":
        if not hasattr(cls, "_instance"):
            cls()

        return cls._instance

    @classmethod
    def save_pref(cls, pref: Pref[Any]) -> None:
        cls.instance().store_setting(pref.fqdn, pref.value)

    @classmethod
    def load_pref(cls, pref: Pref[Any]) -> None:
        pref.value = pref.data_type(cls.instance().get_setting(pref.fqdn, pref.value))

    @classmethod
    def load_group(cls, group: PrefsGroup) -> None:
        for item in group.items:
            cls.load_pref(item)

    @classmethod
    def load_config(cls, config: PrefsConfig) -> None:
        for group in config:
            cls.load_group(group)

    def __init__(self) -> None:
        super().__init__(parent=QCoreApplication.instance())
