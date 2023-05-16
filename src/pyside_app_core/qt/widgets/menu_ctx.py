import contextlib
from typing import ContextManager

from PySide6 import QtGui
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMenu,
    QMenuBar,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from pyside_app_core.qt.util.pixel_val import PixelVal
from pyside_app_core.qt.util.s_color import SColor
from pyside_app_core.qt.widgets.object_name_mixin import ObjectNameMixin


class MenuContext(QMenu):
    @contextlib.contextmanager
    def add_menu(self, name: str) -> ContextManager["MenuContext"]:
        menu = MenuContext(name, self)
        menu.setObjectName(f"Menu{name.replace(' ', '_')}")
        yield menu
        self.addMenu(menu)

    @contextlib.contextmanager
    def add_action(self, name: str) -> ContextManager[QAction]:
        action = QtGui.QAction(name, self)
        action.setObjectName(f"MenuAction{name.replace(' ', '_')}")
        yield action
        self.addAction(action)


class MenuBarContext(ObjectNameMixin, QWidget):
    def __init__(
        self, parent: QWidget, border_width=PixelVal(2), border_color=SColor(20, 20, 20)
    ):
        super(MenuBarContext, self).__init__(parent=parent)

        self._border_width = border_width
        self.setStyleSheet(
            f"""
            #{self.obj_name} {{
                border-bottom: {border_width} solid {border_color};
            }}
            """
        )

        self.setContentsMargins(0, 0, 0, 0)

        self._layout = QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._layout.addStretch()

        self._menu_layout = QHBoxLayout()
        self._menu_layout.setSpacing(0)
        self._menu_layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addLayout(self._menu_layout)

        self._shift = QWidget(self)
        self._menu_layout.addWidget(self._shift)
        self._shift.setFixedWidth(0)

        self._menu_bar = QMenuBar(parent=parent)
        self._menu_bar.setSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.MinimumExpanding
        )
        self._menu_layout.addWidget(self._menu_bar)

        self._menu_layout.addStretch()

        self._layout.addStretch()

    def setNativeMenuBar(self, val: bool):
        self._menu_bar.setNativeMenuBar(val)

    @contextlib.contextmanager
    def add_menu(self, name: str) -> ContextManager[MenuContext]:
        menu = MenuContext(name, self)
        menu.setObjectName(f"Menu{name.replace(' ', '_')}")
        yield menu
        self._menu_bar.addMenu(menu)

    @contextlib.contextmanager
    def add_action(self, name: str) -> ContextManager[QAction]:
        action = QtGui.QAction(name, self)
        action.setObjectName(f"MenuBarAction{name.replace(' ', '_')}")
        yield action
        self._menu_bar.addAction(action)

    def set_offset(self, val: int):
        self.setFixedHeight(val + self._border_width)

    def set_shift(self, val: int):
        self._shift.setFixedWidth(val)
