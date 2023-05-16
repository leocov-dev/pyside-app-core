import contextlib
from typing import ContextManager, Literal

from PySide6 import QtGui
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QToolBar

from pyside_app_core.qt.widgets.object_name_mixin import ObjectNameMixin
from pyside_app_core.services import application_service

ToolBarArea = Literal["top", "bottom", "left", "right"]

_TOOL_BAR_AREA_MAP = {
    "top":    Qt.ToolBarArea.TopToolBarArea,
    "bottom": Qt.ToolBarArea.BottomToolBarArea,
    "right":  Qt.ToolBarArea.RightToolBarArea,
    "left":   Qt.ToolBarArea.LeftToolBarArea,
}


class ToolBarContext(ObjectNameMixin, QToolBar):
    def __init__(
        self, area: ToolBarArea, parent: QMainWindow, movable=False
    ):
        self._area = area
        self._theme = application_service.get_app_theme()

        _margins = [1, 1, 1, 1]

        if area == "left":
            self._border_side = "right"
        elif area == "right":
            self._border_side = "left"
        elif area == "top":
            self._border_side = "bottom"
            _margins[1] = 5
        else:
            self._border_side = "top"
            _margins[3] = 5

        self.OBJECT_NAME = f"ToolBar_{area}"
        super(ToolBarContext, self).__init__(self.OBJECT_NAME, parent=parent)

        self.setContentsMargins(*_margins)
        self.setMovable(movable)
        self.setIconSize(QSize(28, 28))

        parent.addToolBar(_TOOL_BAR_AREA_MAP[self._area], self)

        self._setup_style()

    @contextlib.contextmanager
    def add_action(
        self, name: str, icon: QIcon | None = None
    ) -> ContextManager[QtGui.QAction]:
        action = QtGui.QAction(text=name, parent=self)
        action.setObjectName(f"ToolBarAction_{name}")
        if icon:
            action.setIcon(icon)

        yield action
        self.addAction(action)

    def _setup_style(self):
        self.setStyleSheet(
            f"""
#{self.obj_name} {{
    border-{self._border_side}: {self._theme.win_divider_width} solid {self._theme.win_divider_color};
}}
"""
        )
