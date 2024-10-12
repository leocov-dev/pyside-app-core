from collections.abc import Callable

from PySide6.QtWidgets import QComboBox, QWidget

from pyside_app_core.ui.prefs import ItemWidget
from pyside_app_core.ui.prefs.preferences_default_widgets import PrefItemInterface


def ComboItemWidget(options: list[str]) -> Callable[[type], type[ItemWidget]]:
    def _inner(type_: type) -> type:
        if type_ is not int:
            raise TypeError("ComboItemWidget only works with 'int' PrefItem type")

        class _ComboItemWidget(ItemWidget):
            _OPTIONS: list[str] = options

            def __init__(self, item: PrefItemInterface[int], parent: QWidget | None = None):
                super().__init__(item, parent)

                combo = QComboBox(parent=self)
                combo.addItems(self._OPTIONS)
                combo.setCurrentIndex(item.value)
                self.layout().addWidget(combo)

                combo.currentIndexChanged.connect(item.set_value)

        return _ComboItemWidget

    return _inner
