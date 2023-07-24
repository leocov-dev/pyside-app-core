from PySide6.QtCore import QPoint, QRect, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QWidget

from pyside_app_core.qt.widgets.about_dialog import AboutDialog
from pyside_app_core.qt.widgets.frameless.base_window import FramelessBaseMixin
from pyside_app_core.qt.widgets.menu_ctx import MenuBarContext
from pyside_app_core.qt.widgets.tool_bar_ctx import ToolBarContext
from pyside_app_core.qt.widgets.window_settings_mixin import WindowSettingsMixin
from pyside_app_core.services import platform_service


class FramelessMainWindow(WindowSettingsMixin, FramelessBaseMixin, QMainWindow):
    def __init__(self):
        super(FramelessMainWindow, self).__init__(parent=None)

        self._about_dialog = AboutDialog()

        self._central = QWidget(parent=self)
        self._central.setStyleSheet("""background-color: none;""")
        self.setCentralWidget(self._central)

        # must in order to show grab handle
        self.statusBar().show()

        self._menu_bar = MenuBarContext(
            self,
            border_width=0
            if platform_service.is_macos
            else self._theme.win_divider_width,
            border_color=self._theme.win_divider_color,
        )

        self._menu_bar.setNativeMenuBar(platform_service.is_macos)
        self.setMenuWidget(self._menu_bar)

        with self._menu_bar.add_menu(self.tr("File")) as file_menu:
            with file_menu.add_action(self.tr("Quit")) as exit_action:
                exit_action.setMenuRole(QAction.MenuRole.QuitRole)
                exit_action.triggered.connect(self.close)

        with self._menu_bar.add_menu(self.tr("Help")) as help_menu:
            with help_menu.add_action(self.tr("About")) as about_action:
                about_action.setMenuRole(QAction.MenuRole.AboutRole)

                def _show_about():
                    self._about_dialog.exec()

                about_action.triggered.connect(_show_about)

        self._tool_bar = ToolBarContext(area="top", parent=self, movable=False)
        self._tool_bar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)

        if platform_service.is_macos:
            spacer = QWidget(self)
            spacer.setFixedWidth(self._window_actions.container_width + 5)
            spacer.setFixedHeight(28)
            self._tool_bar.addWidget(spacer)

        self._menu_bar.set_offset(
            5 if platform_service.is_macos else self._window_actions.container_height
        )
        self._menu_bar.set_shift(8)

    @property
    def menu_bar(self):
        return self._menu_bar

    @property
    def tool_bar(self):
        return self._tool_bar

    @property
    def window_bar_geo(self) -> QRect:
        return QRect(QPoint(0, 0), self.tool_bar.geometry().bottomRight())
