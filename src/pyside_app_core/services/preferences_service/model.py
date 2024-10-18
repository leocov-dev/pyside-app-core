from collections import defaultdict
from collections.abc import Callable, Iterator, Sequence
from pathlib import Path
from typing import Any, Protocol, Union, cast, overload

from PySide6.QtCore import QModelIndex, QObject, Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QWidget

from pyside_app_core import log
from pyside_app_core.mixin.settings_mixin import SettingsMixin
from pyside_app_core.ui import prefs


class ItemWidgetInterface(Protocol):
    def __init__(self, item: "PrefItem", parent: QWidget | None = None): ...


class PrefItem(Sequence[QStandardItem]):
    @overload
    def __getitem__(self, index: int) -> QStandardItem: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[QStandardItem]: ...

    def __getitem__(self, index: int | slice) -> QStandardItem | Sequence[QStandardItem]:
        return self._row_items[index]

    def __len__(self) -> int:
        return len(self._row_items)

    def __str__(self) -> str:
        return f'{type(self).__name__} "{self.fqdn}" {self.type_} ({self.value})'

    def __init__(
        self,
        name_item: QStandardItem,
        type_item: QStandardItem,
        value_item: QStandardItem,
    ):
        self._row_items: list[QStandardItem] = [
            name_item,
            type_item,
            value_item,
        ]

    @classmethod
    def new(
        cls,
        display_name: str,
        name: str,
        default_value: str | float | bool | Path,
        *,
        widget_class: type[ItemWidgetInterface] | Callable[[type], type[ItemWidgetInterface]] = prefs.auto,
    ) -> "PrefItem":
        name_item = QStandardItem(display_name)
        name_item.setData(name, Qt.ItemDataRole.UserRole)
        name_item.setEditable(False)

        _type = type(default_value)

        if callable(widget_class):
            widget_class = widget_class(_type)  # type: ignore[arg-type, assignment]

        type_item = QStandardItem(_type.__name__)
        type_item.setData(_type, Qt.ItemDataRole.UserRole)
        type_item.setData(widget_class, Qt.ItemDataRole.UserRole + 1)
        type_item.setEditable(False)

        value_item = QStandardItem()

        if issubclass(_type, bool):
            value_item.setText("")
            value_item.setEditable(False)
            value_item.setCheckable(True)
            value_item.setCheckState(Qt.CheckState.Checked if default_value else Qt.CheckState.Unchecked)
        if issubclass(_type, Path):
            value_item.setText("" if default_value == Path() else str(default_value))
            value_item.setData(None if default_value == Path() else default_value, Qt.ItemDataRole.UserRole)
        else:
            value_item.setText(str(default_value))
            value_item.setData(default_value, Qt.ItemDataRole.UserRole)

        return cls(name_item, type_item, value_item)

    @property
    def name_item(self) -> QStandardItem:
        return self._row_items[0]

    @property
    def type_item(self) -> QStandardItem:
        return self._row_items[1]

    @property
    def value_item(self) -> QStandardItem:
        return self._row_items[2]

    @property
    def name(self) -> str:
        return str(self.name_item.data(Qt.ItemDataRole.UserRole))

    @property
    def display_name(self) -> str:
        return self.name_item.text()

    @property
    def type_(self) -> type:
        return cast(type, self.type_item.data(Qt.ItemDataRole.UserRole))

    @property
    def value(self) -> Any:
        if issubclass(self.type_, bool):
            value = Qt.CheckState(self.value_item.checkState()) == Qt.CheckState.Checked
        else:
            value = self.value_item.data(Qt.ItemDataRole.UserRole)
        log.debug(f"PrefItem.value -> {value}")
        return value

    @property
    def fqdn(self) -> str:
        if parent := cast(_Collection, self.name_item.parent()):
            return f"{parent.fqdn}.{self.name}"
        return self.name

    @property
    def widget_class(self) -> type[ItemWidgetInterface]:
        return cast(
            type[ItemWidgetInterface],
            self.type_item.data(Qt.ItemDataRole.UserRole + 1),
        )

    def set_value(self, value: Any) -> None:
        log.debug(f"PrefItem.set_value({value})")
        if issubclass(self.type_, bool):
            self.value_item.setCheckState(Qt.CheckState.Checked if value else Qt.CheckState.Unchecked)
        else:
            self.value_item.setData(value, Qt.ItemDataRole.UserRole)

    def index(self) -> QModelIndex:  # type: ignore[override]
        return self.name_item.index()


class _Collection(QStandardItem):
    def __init__(
        self,
        display_name: str,
        name: str,
    ):
        super().__init__(display_name)
        self.setData(name, Qt.ItemDataRole.UserRole)
        self.setEditable(False)

    @property
    def display_name(self) -> str:
        return self.text()

    @property
    def name(self) -> str:
        return str(self.data(Qt.ItemDataRole.UserRole))

    @property
    def fqdn(self) -> str:
        if self.parent():
            return f"{cast(_Collection, self.parent()).fqdn}.{self.name}"
        return self.name


class PrefGroup(_Collection):
    def __init__(
        self,
        display_name: str,
        name: str,
        items: Sequence[PrefItem],
    ):
        super().__init__(display_name, name)

        for item in items:
            super().appendRow(item)

    def __iter__(self) -> Iterator[PrefItem]:
        for row in range(self.rowCount()):
            name_item = self.child(row, 0)
            type_item = self.child(row, 1)
            value_item = self.child(row, 2)
            yield PrefItem(name_item, type_item, value_item)


class PrefSection(_Collection):
    def __init__(
        self,
        display_name: str,
        name: str,
        items: Sequence[Union["PrefSection", PrefGroup]],
    ):
        super().__init__(display_name, name)

        for item in items:
            super().appendRow(item)

    def __iter__(self) -> Iterator[Union["PrefSection", PrefGroup]]:
        for row in range(self.rowCount()):
            yield cast(
                PrefGroup | PrefSection,
                self.child(row, 0),
            )


class PreferencesModel(SettingsMixin, QStandardItemModel):
    def __init__(self, parent: QObject | None = None):
        super().__init__(parent=parent)
        self.setColumnCount(3)

        self.dataChanged.connect(self._on_data_changed)

    def __iter__(self) -> Iterator[PrefSection | PrefGroup]:
        for row in range(self.invisibleRootItem().rowCount()):
            yield cast(
                PrefGroup | PrefSection,
                self.item(row, 0),
            )

    def clear_all_prefs(self) -> None:
        log.warning("Clearing all settings...")
        self._settings.clear()

    def appendRows(self, items: Sequence[PrefSection | PrefGroup]) -> None:
        for item in items:
            self.invisibleRootItem().appendRow(item)

        # -----
        fqdn_map: dict[str, int] = defaultdict(int)
        for item_ in self.walk():
            fqdn_map[item_.fqdn] += 1

        duplicate = []
        for fqdn, count in fqdn_map.items():
            if count > 1:
                duplicate.append(fqdn)

        if duplicate:
            raise ValueError(f"Duplicate Preference Item Paths: {duplicate}")

        # ----
        for pref in self.walk():
            if isinstance(pref, PrefItem):
                stored_value: Any = self.get_setting(pref.fqdn, pref.value)
                if stored_value != pref.value:
                    self.blockSignals(True)
                    pref.set_value(stored_value)
                    self.blockSignals(False)

    def walk(self) -> Iterator[PrefSection | PrefGroup | PrefItem]:
        def _w(root: PrefSection | PrefGroup | PrefItem) -> Iterator[PrefSection | PrefGroup | PrefItem]:
            yield root
            if isinstance(root, PrefItem):
                return
            for child in root:
                yield from _w(child)

        for item in self:
            yield from _w(item)

    def pref_from_index(self, index: QModelIndex) -> PrefSection | PrefGroup | PrefItem:
        raw_item = super().itemFromIndex(index)
        if isinstance(raw_item, PrefGroup | PrefSection):
            return raw_item

        parent = super().itemFromIndex(index.parent())

        if not isinstance(parent, PrefGroup):
            raise TypeError("given item can't be translated into a PrefItem")

        return PrefItem(
            parent.child(index.row(), 0),
            parent.child(index.row(), 1),
            parent.child(index.row(), 2),
        )

    def _on_data_changed(self, top_left: QModelIndex, bottom_right: QModelIndex, _: list[Qt.ItemDataRole]) -> None:
        log.debug("pref data changed ...")
        if top_left != bottom_right:
            raise ValueError("Can't modify multiple preferences at once")

        item = self.pref_from_index(top_left)
        if not isinstance(item, PrefItem):
            raise TypeError(f"Can't store data changes for non PrefItem: {item}")

        self.store_setting(
            item.fqdn,
            item.value,
        )


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QTreeView

    q_app = QApplication()

    _prefs = PreferencesModel()
    _prefs.appendRows(
        [
            PrefGroup(
                "Application",
                "app",
                [
                    PrefItem.new("Arduino CLI Path", "arduino_cli", Path("~/bin/arduino")),
                    PrefItem.new("Remember last selection", "rem_sel", False),
                ],
            ),
            PrefSection(
                "Tools",
                "tools",
                [
                    PrefGroup(
                        "Calibration",
                        "calibration",
                        [
                            PrefItem.new("Offset Value", "offset", 0),
                            PrefItem.new("Multiplier", "mult", 1),
                        ],
                    )
                ],
            ),
        ]
    )

    view = QTreeView()
    view.setModel(_prefs)

    view.show()

    q_app.exec()
