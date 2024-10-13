from collections.abc import Callable
from pathlib import Path

from PySide6.QtWidgets import QComboBox, QWidget

from pyside_app_core.ui.prefs import ItemWidget
from pyside_app_core.ui.prefs.preferences_default_widgets import PrefItemInterface, _PathItemWidget
from pyside_app_core.ui.widgets.file_picker import FilePicker, FilePickerType


def ComboItemWidget(options: list[str]) -> Callable[[type], type[ItemWidget]]:
    def _inner(type_: type) -> type:
        if not issubclass(type_, int):
            raise TypeError("ComboItemWidget only works with 'int' PrefItem type")

        class _Widget(ItemWidget):
            _OPTIONS: list[str] = options

            def __init__(self, item: PrefItemInterface[int], parent: QWidget | None = None):
                super().__init__(item, parent)

                combo = QComboBox(parent=self)
                combo.addItems(self._OPTIONS)
                combo.setCurrentIndex(item.value)
                self.layout().addWidget(combo)

                combo.currentIndexChanged.connect(item.set_value)

        return _Widget

    return _inner


def PathWithPlaceholder(
    *, placeholder_text: str = "", kind: FilePickerType | None = None
) -> Callable[[type], type[ItemWidget]]:
    def _inner(type_: type) -> type:
        if not issubclass(type_, Path):
            raise TypeError("PathWithPlaceholder only works with 'Path' PrefItem type")

        class _Widget(ItemWidget):
            def __init__(self, item: PrefItemInterface[Path], parent: QWidget | None = None):
                super().__init__(item, parent)

                pht = placeholder_text
                if not pht:
                    if kind == FilePickerType.DIR:
                        pht = "Pick a Directory"
                    elif kind == FilePickerType.FILE:
                        pht = "Pick a File"

                fp = FilePicker(
                    config=kind or _PathItemWidget.make_config(item.value),
                    placeholder=pht,
                    parent=self,
                )
                fp.set_file_path(item.value)
                self.layout().addWidget(fp)

                fp.valueChanged.connect(item.set_value)

        return _Widget

    return _inner
