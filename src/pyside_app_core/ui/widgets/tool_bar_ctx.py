import contextlib
from collections.abc import Generator
from typing import Literal

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QSizePolicy, QToolBar, QWidget

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
        self._actions: dict[str, QAction] = {}
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
        """fixed width constant spacer"""
        spacer = QWidget(self)
        spacer.setDisabled(True)
        spacer.setFixedSize(QSize(width, 1))
        self._spacing_items.append(spacer)
        self.addWidget(spacer)

    def remove_last_spacer(self) -> None:
        spacer = self._spacing_items.pop()
        spacer.deleteLater()

    def setSpacing(self, spacing: int) -> None:
        self._spacing = spacing
        for item in self._spacing_items:
            item.setFixedSize(QSize(spacing, 1))

    def addAction(self, action: QAction) -> None:  # type: ignore[override]
        self._actions[action.text()] = action
        super().addAction(action)
        # custom spacing between widgets
        self.add_spacer(self._spacing)

    @contextlib.contextmanager
    def action(self, name: str, icon: QIcon | None = None) -> Generator[QAction, None, None]:
        if name not in self._actions:
            action = self._actions[name] = QAction(text=name, parent=self)
            action.setObjectName(f"ToolBarAction_{name}")
            self.addAction(action)
        else:
            action = self._actions[name]

        if icon:
            action.setIcon(icon)

        yield action

    def get_action(self, name: str) -> QAction:
        return self._actions[name]
