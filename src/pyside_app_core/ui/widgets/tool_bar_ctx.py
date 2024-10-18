import contextlib
from collections.abc import Iterator
from typing import Literal

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QSizePolicy, QToolBar, QToolButton, QWidget

from pyside_app_core.mixin.object_name_mixin import ObjectNameMixin

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
        self._spacing = 0
        self._spacing_items: list[QWidget] = []

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

    def add_stretch(self) -> None:
        stretch = QWidget(self)
        stretch.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.addWidget(stretch)

    def add_spacer(self, width: int = 10) -> None:
        spacer = QWidget(self)
        spacer.setDisabled(True)
        spacer.setFixedSize(QSize(width, 1))
        self.addWidget(spacer)

    def setSpacing(self, spacing: int) -> None:
        self._spacing = spacing
        for item in self._spacing_items:
            item.setFixedSize(QSize(spacing, 1))

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

        spacer = QWidget(self)
        spacer.setDisabled(True)
        spacer.setFixedSize(QSize(self._spacing, 1))
        self._spacing_items.append(spacer)
        self.addWidget(spacer)
