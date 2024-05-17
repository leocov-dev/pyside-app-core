from typing import Literal

from PySide6.QtCore import Slot
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QButtonGroup, QHBoxLayout, QMenu, QVBoxLayout, QWidget

from pyside_app_core.qt.widgets.dynamic_stacked_widget import DynamicStackedWidget
from pyside_app_core.qt.widgets.object_name_mixin import ObjectNameMixin
from pyside_app_core.qt.widgets.settings_mixin import SettingsMixin
from pyside_app_core.qt.widgets.tool_button import ToolButton

ToolStackSide = Literal["right", "left"]


class ToolStack(SettingsMixin, ObjectNameMixin, QWidget):
    def __init__(
        self,
        side: ToolStackSide,
        parent: QWidget,
        menu: QMenu | None = None,
    ):
        super().__init__(parent=parent)

        # opposite_side = "left" if side == "right" else "right"

        self._menu = menu

        container_layout = QHBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        self.setLayout(container_layout)

        _button_container = QWidget(self)
        _button_container.setObjectName(f"{self.obj_name}_BUTTON_CONTAINER")

        self._button_layout = QVBoxLayout()
        _button_container.setLayout(self._button_layout)
        self._button_layout.setSpacing(8)

        self._button_group = QButtonGroup(self)
        self._button_group.setExclusive(False)

        self._stack = DynamicStackedWidget(self)

        if side == "right":
            self._button_layout.setContentsMargins(10, 10, 10, 3)
            container_layout.addWidget(self._stack)
            container_layout.addWidget(_button_container)
        else:
            self._button_layout.setContentsMargins(10, 10, 10, 3)
            container_layout.addWidget(_button_container)
            container_layout.addWidget(self._stack)

    def add_widget(self, icon: QIcon, widget: QWidget, tooltip: str) -> None:
        container = QWidget(self)
        container.setObjectName(f"{self.obj_name}_CONTAINER")
        container_layout = QVBoxLayout()
        container.setLayout(container_layout)
        container_layout.addWidget(widget)
        container_layout.addStretch()

        index: int = self._stack.addWidget(container)

        button = ToolButton(icon, tooltip, parent=self)
        button.setFixedSize((24, 24))
        button.setCheckable(True)
        self._button_group.addButton(button, index)

        num = self._button_layout.count()

        if num > 0:
            self._button_layout.insertWidget(num - 1, button)
        else:
            button.setChecked(True)
            self._button_layout.addWidget(button)
            self._button_layout.addStretch()

        button.clicked.connect(lambda checked: self._on_click(index, checked))

        if self._menu:
            action = QAction(text=tooltip, parent=self._menu)
            action.triggered.connect(lambda: self._on_menu_click(index))
            self._menu.addAction(action)

    @Slot(int, bool)
    def _on_click(self, index: int, checked: bool) -> None:  # noqa: FBT001
        for i, button in enumerate(self._button_group.buttons()):
            self._stack.setCurrentIndex(index)

            if index == i:
                self._stack.setVisible(checked)
                button.setChecked(checked)

            else:
                button.setChecked(False)

    @Slot(int, bool)
    def _on_menu_click(self, index: int) -> None:
        self._on_click(index, True)
