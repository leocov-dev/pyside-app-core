import contextlib
from collections.abc import Iterator

from PySide6 import QtGui
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QMenu,
    QMenuBar,
    QWidget,
)


class MenuContext(QMenu):
    def __init__(self, name: str, parent: QWidget):
        super().__init__(name, parent)
        self._menu_map: dict[str, MenuContext] = {}
        self._action_map: dict[str, QAction] = {}

    @contextlib.contextmanager
    def menu(self, name: str) -> Iterator["MenuContext"]:
        if name not in self._menu_map:
            self._menu_map[name] = MenuContext(name, self)
            self._menu_map[name].setObjectName(f"Menu_{name.replace(' ', '_')}")
            self.addMenu(self._menu_map[name])

        yield self._menu_map[name]

    @contextlib.contextmanager
    def action(self, name: str) -> Iterator[QAction]:
        if name not in self._action_map:
            self._action_map[name] = QtGui.QAction(name, self)
            self._action_map[name].setObjectName(f"MenuAction_{name.replace(' ', '_')}")
            self.addAction(self._action_map[name])

        yield self._action_map[name]


class MenuBarContext(QMenuBar):
    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)

        self._menu_map: dict[str, MenuContext] = {}

    @contextlib.contextmanager
    def menu(self, name: str) -> Iterator[MenuContext]:
        if name not in self._menu_map:
            self._menu_map[name] = MenuContext(name, self)
            self._menu_map[name].setObjectName(f"Menu_{name.replace(' ', '_')}")
            self.addMenu(self._menu_map[name])

        yield self._menu_map[name]
