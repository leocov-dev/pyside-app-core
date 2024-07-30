from abc import abstractmethod
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Generic, Protocol, TypeVar, cast, overload

from PySide6.QtCore import SignalInstance
from PySide6.QtWidgets import QWidget

from pyside_app_core.types.file_picker import DEFAULT_DIR_CONFIG, DEFAULT_FILE_CONFIG, DirConfig, FileConfig

PrefsValue = str | int | float | bool | Path
_PV_contra = TypeVar("_PV_contra", contravariant=True, bound=PrefsValue)


class PrefWidget(Protocol[_PV_contra]):
    def __init__(self, *args: Any, parent: QWidget, **kwargs: dict[str, Any]) -> None: ...

    def setValue(self, value: _PV_contra) -> None: ...

    @property
    def valueChanged(self) -> SignalInstance: ...


class _Parent(Protocol):
    @property
    def fqdn(self) -> str: ...


class Pref(Generic[_PV_contra]):
    def __init__(
        self,
        name: str,
        default: _PV_contra,
        widget: type[PrefWidget[_PV_contra]] | None = None,
    ) -> None:
        self._name = name
        self._type = type(default)
        self._value = default
        self._widget = widget

        # assigned when building PrefsGroup
        self._parent: _Parent | None = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def data_type(self) -> type[_PV_contra]:
        return self._type

    @property
    def widget(self) -> type[PrefWidget[_PV_contra]] | None:
        return self._widget

    @property
    def parent(self) -> _Parent | None:
        return self._parent

    @property
    def value(self) -> PrefsValue:
        return self._value

    @value.setter
    def value(self, value: _PV_contra) -> None:
        self._value = value

    @property
    def fqdn(self) -> str:
        return f"{self.parent.fqdn}.{self._name}" if self.parent is not None else self._name

    def copy(self, new_default: _PV_contra) -> "Pref[_PV_contra]":
        pref = Pref(
            name=self.name,
            default=new_default,
            widget=self.widget,
        )
        pref._parent = self.parent  # noqa: SLF001
        return pref

    def __str__(self) -> str:
        return f"<{self.fqdn}[{self.data_type.__name__}]> {self.value}"


class FilePref(Pref[_PV_contra]):
    def __init__(
        self,
        name: str,
        default: _PV_contra,
        widget: type[PrefWidget[_PV_contra]] | None = None,
        config: FileConfig = DEFAULT_FILE_CONFIG,
    ) -> None:
        self._name = name
        self._value = default
        self._widget = widget
        self._config = config

    @property
    def config(self) -> FileConfig:
        return self._config


class DirPref(Pref[_PV_contra]):
    def __init__(
        self,
        name: str,
        default: _PV_contra,
        widget: type[PrefWidget[_PV_contra]] | None = None,
        config: DirConfig = DEFAULT_DIR_CONFIG,
    ) -> None:
        self._name = name
        self._value = default
        self._widget = widget
        self._config = config


class PrefsGroup:
    def __init__(
        self,
        name: str,
        items: list[Pref[Any]],
        mode: str = "",
    ) -> None:
        self._name = name
        self._items = []
        for item in items:
            item._parent = self  # noqa: SLF001
            self._items.append(item)

        self._mode = mode

    @property
    def name(self) -> str:
        return self._name

    @property
    def items(self) -> list[Pref[Any]]:
        return self._items

    @property
    def fqdn(self) -> str:
        return self._name

    def __str__(self) -> str:
        return "\n".join([str(i) for i in self.items])


class PrefsConfig(Sequence[PrefsGroup]):
    @overload
    @abstractmethod
    def __getitem__(self, index: int) -> PrefsGroup: ...

    @overload
    @abstractmethod
    def __getitem__(self, index: slice) -> tuple[PrefsGroup]: ...

    def __getitem__(self, index: int | slice) -> PrefsGroup | tuple[PrefsGroup]:
        return self._prefs[index]

    def __len__(self) -> int:
        return len(self._prefs)

    def __init__(self, *prefs: PrefsGroup) -> None:
        self._prefs: tuple[PrefsGroup] = cast(tuple[PrefsGroup], prefs)

    def __str__(self) -> str:
        return "\n".join(
            [
                "Preferences",
                *[str(i) for g in self for i in g.items],
            ]
        )
