import contextlib
from collections.abc import Iterator
from typing import Literal

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QToolBar, QToolButton

from pyside_app_core.qt.widgets.object_name_mixin import ObjectNameMixin

ToolBarArea = Literal["top", "bottom", "left", "right"]

_TOOL_BAR_AREA_MAP = {
    "top": Qt.ToolBarArea.TopToolBarArea,
    "bottom": Qt.ToolBarArea.BottomToolBarArea,
    "right": Qt.ToolBarArea.RightToolBarArea,
    "left": Qt.ToolBarArea.LeftToolBarArea,
}


class ToolBarContext(ObjectNameMixin, QToolBar):
    def __init__(self, area: ToolBarArea, parent: QMainWindow, *, movable: bool = False) -> None:
        self._area = area
        self._actions: list[QAction] = []

        if area == "left":
            self._border_side = "right"
        elif area == "right":
            self._border_side = "left"
        elif area == "top":
            self._border_side = "bottom"
        else:
            self._border_side = "top"

        self.OBJECT_NAME = f"ToolBar_{area}"
        super().__init__(self.OBJECT_NAME, parent=parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setGeometry(10, 10, self.width(), self.height())
        self.setMovable(movable)
        self.setIconSize(QSize(28, 28))

        parent.addToolBar(_TOOL_BAR_AREA_MAP[self._area], self)

    @contextlib.contextmanager
    def add_action(self, name: str, icon: QIcon | None = None) -> Iterator[QAction]:
        action = QAction(text=name, parent=self)
        action.setObjectName(f"ToolBarAction_{name}")
        if icon:
            action.setIcon(icon)

        self._actions.append(action)
        if len(self._actions) == 1:
            _ = next(c for c in self.children() if isinstance(c, QToolButton))
        yield action
        self.addAction(action)
