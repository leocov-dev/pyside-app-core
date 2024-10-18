from collections import defaultdict
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

from PySide6.QtCore import QCoreApplication, QItemSelection, QModelIndex, QObject
from PySide6.QtGui import QStandardItem

from pyside_app_core.services.preferences_service.model import PreferencesModel, PrefGroup, PrefItem, PrefSection

PrefCallback = Callable[[PrefItem], None]


class PreferencesService(QObject):
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
    def add_prefs(cls, *items: PrefSection | PrefGroup) -> None:
        cls.instance()._model.appendRows(items)

    @classmethod
    def model(cls) -> PreferencesModel:
        return cls.instance()._model

    @classmethod
    def fqdn_to_pref(cls, fqdn: str) -> PrefItem | PrefGroup | PrefSection | None:
        return cls.instance()._fqdn_to_item(fqdn)

    @classmethod
    def clear_all(cls) -> None:
        cls.instance()._model.clear_all_prefs()

    @classmethod
    def connect_pref_changed(cls, fqdn: str, cb: PrefCallback) -> None:
        cls.instance()._listeners[fqdn].append(cb)

    def __init__(self) -> None:
        super().__init__(parent=QCoreApplication.instance())

        self._model = PreferencesModel(parent=self)

        self._listeners: dict[str, list[PrefCallback]] = defaultdict(list)

        # ---
        self._model.dataChanged.connect(self._on_change)

    def __len__(self) -> int:
        return self._model.rowCount()

    def __iter__(self) -> Iterator[QStandardItem]:
        return iter(self._model.item(r, 0) for r in range(self._model.rowCount()))

    def __str__(self) -> str:
        return "\n".join(
            [
                "",
                "Preferences:",
                *[f"    {p.fqdn}: {p.value}" for p in self.model().walk() if isinstance(p, PrefItem)],
            ]
        )

    def _on_change(self, tl: QModelIndex, *_: Any) -> None:
        item = self._model.pref_from_index(tl)
        if not isinstance(item, PrefItem):
            return

        for listener in self._listeners[item.fqdn]:
            listener(item)

    def _fqdn_to_item(self, fqdn: str) -> PrefItem | PrefGroup | PrefSection | None:
        for item in self.model().walk():
            if item.fqdn == fqdn:
                return item

        return None


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QTreeView

    from pyside_app_core import log

    q_app = QApplication()

    PreferencesService.add_prefs(
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
        PrefGroup(
            "Application",
            "app",
            [
                PrefItem.new("Arduino CLI Path", "arduino_cli", Path("~/bin/arduino")),
                PrefItem.new("Remember last selection", "rem_sel", False),
            ],
        ),
    )

    view = QTreeView()
    view.setMinimumSize(640, 480)
    view.setModel(PreferencesService.model())

    def _print_fqdn(_sel: QItemSelection) -> None:
        if not _sel.indexes():
            return

        item = PreferencesService.model().pref_from_index(_sel.indexes()[0])

        log.info(item.fqdn)

    view.selectionModel().selectionChanged.connect(_print_fqdn)

    view.show()

    view.expandAll()

    q_app.exec()
