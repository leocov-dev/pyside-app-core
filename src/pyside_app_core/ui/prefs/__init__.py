from pathlib import Path

from pyside_app_core.ui.prefs.preferences_default_widgets import (
    ItemWidget,
    _BoolItemWidget,
    _FloatItemWidget,
    _IntItemWidget,
    _PathItemWidget,
    _StringItemWidget,
)


def auto(_type: type) -> type[ItemWidget]:
    if issubclass(_type, str):
        return _StringItemWidget
    if issubclass(_type, bool):
        return _BoolItemWidget  # QCheckBox
    if issubclass(_type, int):
        return _IntItemWidget  # QSpinBox
    if issubclass(_type, float):
        return _FloatItemWidget  # QDoubleSpinBox
    if issubclass(_type, Path):
        return _PathItemWidget  # FilePicker

    raise TypeError(f"Unsupported type {_type}")
