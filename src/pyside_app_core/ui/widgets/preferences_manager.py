from pathlib import Path
from typing import Any, cast

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QStackedWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from pyside_app_core.errors.basic_errors import PreferencesError
from pyside_app_core.services.preferences_service import PreferencesService
from pyside_app_core.types.preferences import Pref, PrefsConfig, PrefsValue, PrefWidget
from pyside_app_core.ui.widgets.file_picker import FilePicker
from pyside_app_core.ui.widgets.layout import HLine
from pyside_app_core.ui.widgets.pref_check_box import PrefCheckBox
from pyside_app_core.ui.widgets.window_settings_mixin import WindowSettingsMixin


class PreferenceContent(QWidget):
    def __init__(self, group: str, prefs: list[Pref[Any]], parent: QWidget):
        super().__init__(parent=parent)
        self._group = group

        _ly = QVBoxLayout()
        self.setLayout(_ly)

        _heading = QLabel(group)
        _h_font = _heading.font()
        _h_font.setBold(True)
        _heading.setFont(_h_font)
        _ly.addWidget(_heading)

        _ly.addWidget(HLine(self))

        _form = QFormLayout()
        _ly.addLayout(_form)

        for pref in prefs:
            if pref.value is None and pref.widget is None:
                continue
            _form.addRow(pref.name, cast(QWidget, self._build_widget(pref)))

        _ly.addStretch()

    @staticmethod
    def _update_value(value: PrefsValue, pref: Pref[PrefsValue]) -> None:
        pref.value = value
        PreferencesService.save_pref(pref)

    def _build_widget(self, pref: Pref[PrefsValue]) -> PrefWidget[Any]:
        if pref.widget is not None:
            w: PrefWidget[Any] = pref.widget(parent=self)
            w.setValue(pref.value)
            w.valueChanged.connect(lambda v: self._update_value(v, pref))
            return w
        if pref.data_type is bool:
            w: PrefCheckBox = PrefCheckBox(parent=self)  # type: ignore[no-redef]
            w.setValue(pref.value)
            w.valueChanged.connect(lambda v: self._update_value(v, pref))
            return cast(PrefWidget[bool], w)
        if pref.data_type is int:
            w: QSpinBox = QSpinBox(parent=self)  # type: ignore[no-redef]
            w.setValue(pref.value)
            w.valueChanged.connect(lambda v: self._update_value(v, pref))
            return cast(PrefWidget[int], w)
        if pref.data_type is float:
            w: QDoubleSpinBox = QDoubleSpinBox(parent=self)  # type: ignore[no-redef]
            w.setValue(pref.value)
            w.valueChanged.connect(lambda v: self._update_value(v, pref))
            return cast(PrefWidget[float], w)
        if pref.data_type is str:
            w: PrefCheckBox = PrefCheckBox(parent=self)  # type: ignore[no-redef]
            w.setValue(pref.value)
            w.valueChanged.connect(lambda v: self._update_value(v, pref))
            return cast(PrefWidget[str], w)
        if issubclass(pref.data_type, Path):
            w: FilePicker = FilePicker(parent=self)  # type: ignore[no-redef]
            w.setValue(pref.value)
            w.valueChanged.connect(lambda v: self._update_value(v, pref))
            return cast(PrefWidget[Path], w)

        raise PreferencesError(f'"{pref}" is not understood')


class PreferencesManager(WindowSettingsMixin, QWidget):
    def __init__(self, config: PrefsConfig, parent: QWidget | None = None):
        super().__init__(parent=parent)

        self.setWindowTitle("Preferences")

        # ---
        self._config = config

        # ---
        _ly = QHBoxLayout()
        # _ly.setContentsMargins(0, 0, 0, 0)
        self.setLayout(_ly)

        self._group_list = QTreeWidget(self)
        self._group_list.setHeaderHidden(True)
        _ly.addWidget(self._group_list, stretch=1)

        self._pref_stack = QStackedWidget(self)
        _ly.addWidget(self._pref_stack, stretch=4)

        # ---
        for group in config:
            self._add_group(group.name, group.items)

        # ---
        self._group_list.currentItemChanged.connect(self._on_pick)

        self._group_list.setCurrentIndex(
            self._group_list.model().index(self.get_setting("selected-group-idx", 0, int), 0)
        )

    def _add_group(self, group: str, prefs: list[Pref[Any]]) -> None:
        stack_idx = self._pref_stack.addWidget(PreferenceContent(group, prefs, self))

        grp = QTreeWidgetItem()
        grp.setText(0, group)
        grp.setData(0, Qt.ItemDataRole.UserRole, stack_idx)
        self._group_list.addTopLevelItem(grp)

    def _on_pick(self, current: QTreeWidgetItem, _: QTreeWidgetItem) -> None:
        idx: int = current.data(0, Qt.ItemDataRole.UserRole)
        self._pref_stack.setCurrentIndex(idx)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.store_setting("selected-group-idx", self._pref_stack.currentIndex())
        return super().closeEvent(event)
