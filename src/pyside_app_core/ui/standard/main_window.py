import contextlib
from collections.abc import Generator
from typing import Any

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QAction, QCloseEvent, QDesktopServices, QResizeEvent
from PySide6.QtWidgets import QApplication, QDialog, QGraphicsBlurEffect, QMainWindow, QProgressBar, QWidget

from pyside_app_core.app import AppMetadata
from pyside_app_core.services import platform_service
from pyside_app_core.ui.standard.about_dialog import AboutDialog
from pyside_app_core.ui.standard.base_window import BaseMixin, Shade
from pyside_app_core.ui.widgets.menu_ctx import MenuBarContext
from pyside_app_core.ui.widgets.tool_bar_ctx import ToolBarContext
from pyside_app_core.ui.widgets.window_settings_mixin import WindowSettingsMixin


class MainWindow(WindowSettingsMixin, BaseMixin, QMainWindow):
    def __init__(self) -> None:
        super().__init__(parent=None)

        self._shade = Shade(self)
        self.setGraphicsEffect(self._shade.gfx())

        self.setCentralWidget(QWidget(self))

        # must call in order to show grab handle
        self.statusBar().show()

        self._progress = QProgressBar(self)
        self._progress.setHidden(True)
        self.statusBar().addPermanentWidget(self._progress)

        self._menu_bar = MenuBarContext(self)
        self._menu_bar.setNativeMenuBar(platform_service.is_macos)
        self.setMenuBar(self._menu_bar)

        with (
            self._menu_bar.menu("File") as file_menu,
            file_menu.action("Quit") as exit_action,
        ):
            exit_action.setMenuRole(QAction.MenuRole.QuitRole)
            exit_action.triggered.connect(self.close)

        self._build_menus()

        with self._menu_bar.menu("Window") as window_menu:
            with window_menu.action("Minimize") as min_action:
                min_action.setShortcut("Ctrl+M")
                min_action.triggered.connect(self.showMinimized)
            with window_menu.action("Zoom") as zoom_action:
                zoom_action.triggered.connect(self.showMaximized)

        with self._menu_bar.menu("Help") as help_menu:
            with help_menu.action("About") as about_action:
                about_action.setMenuRole(QAction.MenuRole.AboutRole)
                about_action.triggered.connect(lambda: self.show_app_modal_dialog(self.about_dialog()))

            if AppMetadata.help_url:
                with help_menu.action("Get Help") as help_action:
                    help_action.triggered.connect(lambda: QDesktopServices.openUrl(QUrl(AppMetadata.help_url)))

            if AppMetadata.bug_report_url:
                with help_menu.action("Report Bug") as help_action:
                    help_action.triggered.connect(lambda: QDesktopServices.openUrl(QUrl(AppMetadata.bug_report_url)))

    @property
    def menu_bar(self) -> MenuBarContext:
        return self._menu_bar

    def _build_menus(self) -> None:
        pass

    @staticmethod
    def about_dialog() -> AboutDialog:
        return AboutDialog()

    def closeEvent(self, event: QCloseEvent) -> None:
        super().closeEvent(event)
        QApplication.quit()

    def shade(self, value: bool) -> None:
        self._shade.setVisible(value)
        self._shade.raise_()
        if value:
            self.graphicsEffect().setBlurRadius(2)
        else:
            self.graphicsEffect().setBlurRadius(0)

    def graphicsEffect(self) -> QGraphicsBlurEffect:
        return super().graphicsEffect()  # type: ignore[return-value]

    @contextlib.contextmanager
    def shade_ctx(self) -> Generator[None, None, None]:
        self.shade(True)
        yield
        self.shade(False)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self._shade.update_size()

    def show_app_modal_dialog(self, dialog: QDialog) -> int:
        with self.shade_ctx():
            dialog.setModal(True)
            return dialog.exec()

    def progress_tick(self, value: int, maximum: int) -> None:
        self._progress.setMinimum(0)
        self._progress.setMaximum(maximum)
        self._progress.setValue(value)

        self._progress.setVisible(value != maximum)


class MainToolbarWindow(MainWindow):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self._tool_bar = ToolBarContext(area="top", parent=self, movable=False)
        self._tool_bar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)

        self._build_toolbar()

        self.tool_bar.remove_last_spacer()

    @property
    def tool_bar(self) -> ToolBarContext:
        return self._tool_bar

    def _build_toolbar(self) -> None:
        pass
