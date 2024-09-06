from __future__ import annotations

from enum import IntEnum
from typing import Any, Iterator, cast

from PySide6.QtCore import QCoreApplication, QObject, Qt, Signal, QAbstractProxyModel
from PySide6.QtGui import QStandardItem, QStandardItemModel

from pyside_app_core.mixin.settings_mixin import SettingsMixin
from pyside_app_core.utils.property import ro_classproperty


class PrefRole(IntEnum):
    DISPLAY_NAME = Qt.ItemDataRole.DisplayRole
    NAME = Qt.ItemDataRole.UserRole + 1
    DTYPE = Qt.ItemDataRole.UserRole + 2
    EDITOR_WIDGET = Qt.ItemDataRole.UserRole + 3
    VALUE = Qt.ItemDataRole.UserRole + 4


class Node(SettingsMixin, QStandardItem):

    def __init__(
        self,
        name: str,
        display_name: str,
        *children: Node
    ):
        super().__init__()
        self.setData(name, PrefRole.NAME)
        self.setData(display_name, PrefRole.DISPLAY_NAME)

        self.appendRows(children)

    @property
    def name(self) -> str:
        return self.data(PrefRole.NAME)

    @property
    def display_name(self) -> str:
        return self.data(PrefRole.DISPLAY_NAME)

    @property
    def fqdn(self) -> str:
        return f"{self.parent().fqdn}.{self.name}" if self.parent() is not None else self.name

    @property
    def level(self) -> int:
        def _lvl(node, lvl):
            if node and node.parent():
                return _lvl(node.parent(), lvl + 1)
            return lvl

        return _lvl(self, 0)

    def __str__(self):
        children = "\n".join(
            str(self.child(r, 0)) for r in range(self.rowCount())
        )
        return f"[{self.level}] {' '*self.level*2}{self.name}:\n{children}"


class PrefGroup(Node):
    def __init__(
        self,
        name: str,
        display_name: str,
        *children: Node
    ):
        super().__init__(
            name,
            display_name,
            *children,
        )


class PrefValue(Node):
    def __init__(
        self,
        name: str,
        display_name: str,
        default_value: PrefsValue,
        widget: type[PrefWidget[PrefsValue]] | None = None,
        *children: Node
    ):
        super().__init__(
            name,
            display_name,
            *children,
        )
        self.setData(type(default_value), PrefRole.DTYPE)
        self.setData(widget, PrefRole.EDITOR_WIDGET)

        # update from local storage ----
        self.setData(self.data_type(self.get_setting(self.fqdn, default_value)), PrefRole.VALUE)

    def setData(self, value: Any, role=Qt.ItemDataRole):
        if role == PrefRole.VALUE:
            self.store_setting(self.fqdn, value)
        super().setData(value, role)

    @property
    def data_type(self) -> type[PrefsValue]:
        return self.data(PrefRole.DTYPE)

    @property
    def widget(self) -> type[PrefWidget[PrefsValue]] | None:
        return self.data(PrefRole.EDITOR_WIDGET)

    @property
    def value(self) -> PrefsValue:
        return self.data(PrefRole.VALUE)

    def __str__(self):
        children = "\n".join(
            str(self.child(r, 0)) for r in range(self.rowCount())
        )
        return f"[{self.level}] {' '*self.level*2}{self.name}: \"{self.fqdn}\" {self.data_type.__name__}<{self.value}>{children}"


class PrefGroupsProxy(QAbstractProxyModel):

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self._root = None

    def setRootIndex(self, index: QModelIndex):


    def mapToSource(self, proxyIndex: QModelIndex) -> QModelIndex:
        pass

    def mapFromSource(self, source: QModelIndex) -> QModelIndex:
        pass


class PreferencesService(QObject):
    _pref_changed = Signal(str, object)  # type: ignore[arg-type]

    def __new__(cls) -> "PreferencesService":
        if hasattr(cls, "_instance"):
            raise TypeError(f"Get the instance via {cls.__name__}.instance()")

        cls._instance = super().__new__(cls)
        return cls._instance

    @ro_classproperty
    def pref_changed(cls) -> Signal:
        return cls.instance()._pref_changed

    @classmethod
    def instance(cls) -> "PreferencesService":
        if not hasattr(cls, "_instance"):
            cls()

        return cls._instance

    @classmethod
    def add_groups(cls, *groups: PrefGroup) -> None:
        cls.instance()._model.invisibleRootItem().appendRows(list(groups))

    @classmethod
    def model(cls) -> QStandardItemModel:
        return cls.instance()._model

    def __init__(self) -> None:
        super().__init__(parent=QCoreApplication.instance())

        self._model = QStandardItemModel(parent=self)

    def __getitem__(
        self,
        key: str,
    ) -> PrefGroup:
        return self._model[key]

    def __len__(self) -> int:
        return self._model.rowCount()

    def __iter__(self) -> Iterator[PrefGroup]:
        return iter(cast(PrefGroup, self._model.item(r, 0)) for r in range(self._model.rowCount()))

    def __str__(self) -> str:
        return "\n".join(
            [
                "Preferences:",
                *[str(g) for g in self],
            ]
        )
