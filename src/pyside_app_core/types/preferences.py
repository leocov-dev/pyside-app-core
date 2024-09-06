from pathlib import Path
from typing import Any, Protocol, TypeVar

from PySide6.QtCore import SignalInstance
from PySide6.QtWidgets import QWidget

PrefsValue = str | int | float | bool | Path
_PV_contra = TypeVar("_PV_contra", contravariant=True, bound=PrefsValue)


class PrefWidget(Protocol[_PV_contra]):
    def __init__(self, *args: Any, parent: QWidget, **kwargs: dict[str, Any]) -> None: ...

    def setValue(self, value: _PV_contra) -> None: ...

    @property
    def valueChanged(self) -> SignalInstance: ...
