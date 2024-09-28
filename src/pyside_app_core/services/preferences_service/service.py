from collections.abc import Iterator
from pathlib import Path

from PySide6.QtCore import QCoreApplication, QItemSelection, QObject, Signal
from PySide6.QtGui import QStandardItem

from pyside_app_core.services.preferences_service.model import PreferencesModel, PrefGroup, PrefItem, PrefSection
from pyside_app_core.utils.property import ro_classproperty


class PreferencesService(QObject):
    _pref_changed = Signal(str, object)

    def __new__(cls) -> "PreferencesService":
        if hasattr(cls, "_instance"):
            raise TypeError(f"Get the instance via {cls.__name__}.instance()")

        cls._instance = super().__new__(cls)
        return cls._instance

    @ro_classproperty
    def pref_changed(cls) -> Signal:  # noqa: N805
        return cls.instance()._pref_changed  # type: ignore[return-value]

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

    def __init__(self) -> None:
        super().__init__(parent=QCoreApplication.instance())

        self._model = PreferencesModel(parent=self)

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
