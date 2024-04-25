import contextlib
from typing import ContextManager, List, Literal

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMainWindow, QToolBar, QToolButton

from pyside_app_core.qt.widgets.object_name_mixin import ObjectNameMixin
from pyside_app_core.qt import application_service

ToolBarArea = Literal["top", "bottom", "left", "right"]

_TOOL_BAR_AREA_MAP = {
    "top": Qt.ToolBarArea.TopToolBarArea,
    "bottom": Qt.ToolBarArea.BottomToolBarArea,
    "right": Qt.ToolBarArea.RightToolBarArea,
    "left": Qt.ToolBarArea.LeftToolBarArea,
}


class ToolBarContext(ObjectNameMixin, QToolBar):
    def __init__(self, area: ToolBarArea, parent: QMainWindow, movable=False):
        self._area = area
        self._theme = application_service.get_app_theme()
        self._actions: List[QAction] = []

        if area == "left":
            self._border_side = "right"
        elif area == "right":
            self._border_side = "left"
        elif area == "top":
            self._border_side = "bottom"
        else:
            self._border_side = "top"

        self.OBJECT_NAME = f"ToolBar_{area}"
        super(ToolBarContext, self).__init__(self.OBJECT_NAME, parent=parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setGeometry(10, 10, self.width(), self.height())
        self.setMovable(movable)
        self.setIconSize(QSize(28, 28))

        parent.addToolBar(_TOOL_BAR_AREA_MAP[self._area], self)

        self._setup_style()

    @contextlib.contextmanager
    def add_action(
        self, name: str, icon: QIcon | None = None
    ) -> ContextManager[QAction]:
        action = QAction(text=name, parent=self)
        action.setObjectName(f"ToolBarAction_{name}")
        if icon:
            action.setIcon(icon)

        self._actions.append(action)
        if len(self._actions) == 1:
            _ = [c for c in self.children() if isinstance(c, QToolButton)][0]
        yield action
        self.addAction(action)

    def _setup_style(self):
        self.setStyleSheet(
            f"""
QToolBar#{self.obj_name} {{
    border-{self._border_side}: {self._theme.win_divider_width} solid {self._theme.win_divider_color};
}}
QToolBar#{self.obj_name} > QToolButton {{
    margin-left: 0px;
    margin-top: 10px;
    margin-bottom: 10px;
    spacing: 0;
}}
QToolButton:first {{
    background-color: red;
}}
"""
        )
