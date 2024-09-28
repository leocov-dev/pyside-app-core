from collections.abc import Generator
from typing import cast

from PySide6.QtCore import (
    QItemSelection,
    QItemSelectionModel,
    QModelIndex,
    QPersistentModelIndex,
    QSortFilterProxyModel,
    Qt,
)
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QSizePolicy, QSplitter, QStackedWidget, QTreeView, QVBoxLayout, QWidget

from pyside_app_core.services.preferences_service import PreferencesService, PrefGroup, PrefSection
from pyside_app_core.services.preferences_service.default_editor import DefaultPreferencesPage
from pyside_app_core.services.preferences_service.model import PreferencesModel
from pyside_app_core.services.preferences_service.section_list import SectionListPage
from pyside_app_core.ui.widgets.window_settings_mixin import WindowSettingsMixin

_mgr = None


class PreferencesManager(WindowSettingsMixin, QWidget):
    @classmethod
    def open(cls) -> None:
        global _mgr
        if _mgr is not None:
            _mgr.close()
            _mgr.deleteLater()

        _mgr = PreferencesManager()
        _mgr.show()

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent=parent)

        self.setWindowTitle("Preferences")
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

        # ---
        _ly = QVBoxLayout()
        # _ly.setContentsMargins(0, 0, 0, 0)
        self.setLayout(_ly)

        self._split = QSplitter(Qt.Orientation.Horizontal, parent=self)
        _ly.addWidget(self._split)

        self._group_list = QTreeView(self)
        self._group_list.setHeaderHidden(True)
        self._group_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._split.addWidget(self._group_list)

        self._stack = QStackedWidget()
        self._stack.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._split.addWidget(self._stack)

        self._section_list = SectionListPage(self)
        self._stack.addWidget(self._section_list)

        self._editor = DefaultPreferencesPage(self)
        self._stack.addWidget(self._editor)

        # ---
        self._split.setCollapsible(0, False)
        self._split.setCollapsible(1, False)
        self._proxy = _OnlyGroupsProxy(self)
        self._group_list.setModel(self._proxy)
        self._proxy.setSourceModel(PreferencesService.model())
        self._group_list.expandAll()

        # ---
        self._group_list.selectionModel().selectionChanged.connect(self._on_pick)
        self._section_list.navigate.connect(self._on_navigate)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)

        def _traverse(p: QModelIndex) -> Generator[tuple[int, QModelIndex, QModelIndex], None, None]:
            for r in range(self._proxy.rowCount(p)):
                idx = self._proxy.index(r, 0, p)
                yield r, p, idx
                yield from _traverse(self._proxy.index(r, 0, p))

        max_w = 0

        for row, root, index in _traverse(QModelIndex()):
            self._group_list.setFirstColumnSpanned(row, root, True)
            hint = self._group_list.sizeHintForIndex(index)
            max_w = max(max_w, hint.width())

        if max_w:
            self._group_list.setMinimumWidth(max_w)
            self._split.setSizes([max_w, max_w * 2])

        prev_fqdn = self.get_setting("selected-item-idx", "", str)
        if previous_item := PreferencesService.fqdn_to_pref(prev_fqdn):
            select_index = self._proxy.mapFromSource(previous_item.index())
        else:
            select_index = self._proxy.index(0, 0)

        self._group_list.selectionModel().select(
            select_index,
            QItemSelectionModel.SelectionFlag.ClearAndSelect,
        )

    def _on_pick(self, selected: QItemSelection, _: QItemSelection) -> None:
        if indexes := selected.indexes():
            source_index = self._proxy.mapToSource(indexes[0])
            item = cast(
                PrefSection | PrefGroup,
                PreferencesService.model().itemFromIndex(source_index),
            )

            if isinstance(item, PrefGroup):
                self._stack.setCurrentIndex(1)
                self._editor.set_group(item)
            else:
                self._stack.setCurrentIndex(0)
                self._section_list.set_section(item)

            self.store_setting("selected-item-idx", item.fqdn)

    def _on_navigate(self, item: PrefGroup | PrefSection) -> None:
        self._group_list.selectionModel().select(
            self._proxy.mapFromSource(item.index()),
            QItemSelectionModel.SelectionFlag.ClearAndSelect,
        )


class _OnlyGroupsProxy(QSortFilterProxyModel):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

    def setSourceModel(self, source_model: PreferencesModel) -> None:  # type: ignore[override]
        super().setSourceModel(source_model)

    def sourceModel(self) -> PreferencesModel:
        return cast(PreferencesModel, super().sourceModel())

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex | QPersistentModelIndex) -> bool:
        source_index = self.sourceModel().index(source_row, 0, source_parent)
        return self.sourceModel().rowCount(source_index) > 0
